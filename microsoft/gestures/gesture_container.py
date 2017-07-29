from microsoft.gestures.fingertip_placement_relation import FingertipPlacementRelation
from microsoft.gestures.fingertip_distance_relation import FingertipDistanceRelation
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from microsoft.gestures.relative_placement import RelativePlacement
from microsoft.gestures.any_finger_context import AnyFingerContext
from microsoft.gestures.any_finger_context import AnyFingerContext
from microsoft.gestures.relative_distance import RelativeDistance
from microsoft.gestures.hand_part_motion import HandPartMotion
from microsoft.gestures.any_hand_context import AnyHandContext
from microsoft.gestures.pose_direction import PoseDirection
from microsoft.gestures.finger_flexion import FingerFlexion
from microsoft.gestures.finger_pose import FingerPose
from microsoft.gestures.palm_pose import PalmPose
from microsoft.gestures.finger import Finger
from xml.dom import minidom


class GestureContainer(object):
    def __init__(self, gesture, is_global, pid):
        self._gesture = gesture
        self._is_global = is_global
        self._pid = pid

    @property
    def name(self):
        return self._gesture._name

    def to_xaml(self):
        xml_str = ''
        root = Element('Gesture')
        root.set('xmlns', 'http://schemas.microsoft.com/gestures/2015/xaml')
        root.set('Name', self.name)
        segmens = SubElement(root, 'Gesture.Segments')
        idle = SubElement(segmens, 'IdleGestureSegment')
        idle.set('Name', 'Idle')
        for pose in self._gesture._segments:
            pose_element = SubElement(segmens, pose.__class__.__name__)
            pose_element.set('Name', pose._name)
            for constraint in pose._constrains:
                constraint_element = SubElement(pose_element, constraint.__class__.__name__)
                if isinstance(constraint._context, AnyHandContext):
                    constraint_element.set('Context', '{AnyHand}')
                elif isinstance(constraint._context, AnyFingerContext):
                    constraint_element.set('Context', '{AnyFinger %s}' % (', '.join(map(lambda x: self._get_bitmask_keys_from_dict(Finger, x), constraint._context))))
                else:
                    constraint_element.set('Context', ', '.join(map(lambda x: self._get_bitmask_keys_from_dict(Finger, x), constraint._context)))
                if isinstance(constraint, HandPartMotion):
                    constraint_element.set('MotionScript', ', '.join(map(lambda x: x._name, constraint._motion_script._motion_segments)))
                if isinstance(constraint, FingerPose):
                    if constraint._pose_direction:
                        constraint_element.set('Direction', self._get_bitmask_keys_from_dict(PoseDirection, constraint._pose_direction))
                    constraint_element.set('Flexion', self._get_key_from_dict(FingerFlexion, constraint._finger_flextion))
                if isinstance(constraint, PalmPose):
                    if constraint._direction:
                        constraint_element.set('Direction', self._get_bitmask_keys_from_dict(PoseDirection, constraint._direction))
                    constraint_element.set('Orientation', self._get_bitmask_keys_from_dict(PoseDirection, constraint._orientation))                    
                if hasattr(constraint, '_other_context') and constraint._other_context:
                    constraint_element.set('OtherContext', ', '.join(map(lambda x: self._get_bitmask_keys_from_dict(Finger, x), constraint._other_context)))
                if hasattr(constraint, '_distance') and isinstance(constraint, FingertipPlacementRelation):
                    constraint_element.set('PlacementRelation', self._get_bitmask_keys_from_dict(RelativePlacement, constraint._distance))
                if hasattr(constraint, '_distance') and isinstance(constraint, FingertipDistanceRelation):
                    constraint_element.set('DistanceRelation', self._get_bitmask_keys_from_dict(RelativeDistance, constraint._distance))

        connections = SubElement(root, 'Gesture.SegmentsConnections')
        for connection in self._gesture._segment_connections:
            from_, to_ = connection['From'], connection['To']
            connection_element = SubElement(connections, 'SegmentConnections')
            connection_element.set('From', from_)
            connection_element.set('To', to_)

        xml_str = tostring(root, 'utf-8')
        pretty = minidom.parseString(xml_str)
        return pretty.toprettyxml(indent="  ").replace('\n', '').replace('<?xml version="1.0" ?>', '').strip()

    @staticmethod
    def _get_key_from_dict(cls, value):
        d = cls.__dict__
        for k, v in filter(lambda _: isinstance(_[1], int), d.iteritems()):
            if v == value:
                return k


    @staticmethod
    def _get_bitmask_keys_from_dict(cls, value):
        d = cls.__dict__
        values = [x for x in d.values() if isinstance(x, int)]
        keys = []
        for k, v in filter(lambda x: isinstance(x[1], int), d.iteritems()):
            if v & value != 0 or (v == 0 and value == 0):
                keys.append(k)    
        return '|'.join(keys)