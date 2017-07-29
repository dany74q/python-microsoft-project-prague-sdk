from microsoft.gestures.motion_segment import MotionSegment


class VerticalMotionSegment(MotionSegment):
    Right = None
    Left = None
    Upward = None
    Downward = None
    DiagonalRightUpward = None
    DiagonalRightDownward = None
    DiagonalLeftUpward = None
    DiagonalLeftDownward = None
    ClockwiseArcRightDownward = None
    ClockwiseArcRightUpward = None
    ClockwiseArcLeftDownward = None
    ClockwiseArcLeftUpward = None
    CounterClockwiseArcRightDownward = None
    CounterClockwiseArcRightUpward = None
    CounterClockwiseArcLeftDownward = None
    CounterClockwiseArcLeftUpward = None
    
    def __init__(self, name):
        self._name = name

VerticalMotionSegment.Right = VerticalMotionSegment('Right')
VerticalMotionSegment.Left = VerticalMotionSegment('Left')
VerticalMotionSegment.Upward = VerticalMotionSegment('Upward')
VerticalMotionSegment.Downward = VerticalMotionSegment('Downward')
VerticalMotionSegment.DiagonalRightUpward = VerticalMotionSegment('DiagonalRightUpward')
VerticalMotionSegment.DiagonalRightDownward = VerticalMotionSegment('DiagonalRightDownward')
VerticalMotionSegment.DiagonalLeftUpward = VerticalMotionSegment('DiagonalLeftUpward')
VerticalMotionSegment.DiagonalLeftDownward = VerticalMotionSegment('DiagonalLeftDownward') 
VerticalMotionSegment.ClockwiseArcRightDownward = VerticalMotionSegment('ClockwiseArcRightDownward')
VerticalMotionSegment.ClockwiseArcRightUpward = VerticalMotionSegment('ClockwiseArcRightUpward')
VerticalMotionSegment.ClockwiseArcLeftDownward = VerticalMotionSegment('ClockwiseArcLeftDownward')
VerticalMotionSegment.ClockwiseArcLeftUpward = VerticalMotionSegment('ClockwiseArcLeftUpward')
VerticalMotionSegment.CounterClockwiseArcRightDownward = VerticalMotionSegment('CounterClockwiseArcRightDownward')
VerticalMotionSegment.CounterClockwiseArcRightUpward = VerticalMotionSegment('CounterClockwiseArcRightUpward')
VerticalMotionSegment.CounterClockwiseArcLeftDownward = VerticalMotionSegment('CounterClockwiseArcLeftDownward')
VerticalMotionSegment.CounterClockwiseArcLeftUpward = VerticalMotionSegment('CounterClockwiseArcLeftUpward')