from microsoft.gestures.pose_constraint import PoseConstraint


class FingertipPlacementRelation(PoseConstraint):
    def __init__(self, fingers, relative_placement, other_fingers=()):
        super(FingertipPlacementRelation, self).__init__(fingers, relative_placement, other_fingers)

