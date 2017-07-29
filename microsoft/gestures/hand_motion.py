from microsoft.gestures.gesture_segment import GestureSegment


class HandMotion(GestureSegment):
    def __init__(self, name, *motion_constrains):
        super(HandMotion, self).__init__(name)
        self._constrains = motion_constrains
