from microsoft.gestures.pose_direction import PoseDirection
import collections


class FingerPose(object):
    def __init__(self, fingers, finger_flexion, pose_direction=PoseDirection.Undefined):
        self._context = fingers if isinstance(fingers, collections.Iterable) or not fingers else [fingers]
        self._finger_flextion = finger_flexion
        self._pose_direction = pose_direction
