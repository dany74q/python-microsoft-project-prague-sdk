from microsoft.gestures.finger import Finger


class AllFingersContext(list):
    def __init__(self, fingers=filter(lambda x: isinstance(x, int), Finger.__dict__.values())):
        super(AllFingersContext, self).__init__()
        self.extend(sorted(fingers))
