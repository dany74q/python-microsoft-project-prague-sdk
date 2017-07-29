from microsoft.gestures.gesture_segment import GestureSegment


class HandPose(GestureSegment):
    def __init__(self, name, *pose_constrains):
        super(HandPose, self).__init__(name)
        self._constrains = pose_constrains