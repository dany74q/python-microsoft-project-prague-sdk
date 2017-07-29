from microsoft.gestures.pose_constraint import PoseConstraint

class FingertipDistanceRelation(PoseConstraint):
    def __init__(self, fingers, relative_distance, other_fingers=()):
        super(FingertipDistanceRelation, self).__init__(fingers, relative_distance, other_fingers)

