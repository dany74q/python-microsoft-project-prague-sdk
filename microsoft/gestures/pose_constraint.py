import collections

class PoseConstraint(object):
    def __init__(self, context, distance, other_context):
        self._context = context if isinstance(context, collections.Iterable) or not context else [context]
        self._distance = distance
        self._other_context = other_context if isinstance(other_context, collections.Iterable) or not other_context else [other_context]