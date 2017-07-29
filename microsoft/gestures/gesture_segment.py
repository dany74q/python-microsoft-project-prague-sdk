class GestureSegment(object):
    def __init__(self, name):
        self._name = name
        self._on_triggered = None

    def on_triggered(self, callback):
        self._on_triggered = callback