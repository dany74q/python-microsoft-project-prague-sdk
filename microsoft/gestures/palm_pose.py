from microsoft.gestures.pose_direction import PoseDirection


class PalmPose(object):
    def __init__(self, hand_context, pose_direction=PoseDirection.Undefined, pose_orientation=PoseDirection.Undefined):
        self._context = hand_context
        self._direction = pose_direction
        self._orientation = pose_orientation
