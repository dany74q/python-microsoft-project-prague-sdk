from microsoft.gestures.vertical_motion_segment import VerticalMotionSegment
from microsoft.gestures.vertical_motion_script import VerticalMotionScript
from microsoft.gestures.hand_part_motion import HandPartMotion
from microsoft.gestures.any_hand_context import AnyHandContext

class PalmMotion(HandPartMotion):
    def __init__(self, context, *motion_segments):
        assert motion_segments
        if isinstance(motion_segments[0], VerticalMotionSegment):
            super(PalmMotion, self).__init__(context, VerticalMotionScript(*motion_segments))
