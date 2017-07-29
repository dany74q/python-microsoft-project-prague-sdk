class Gesture(object):
    def __init__(self, name, *segments):
        self._name = name
        self._segments = [x for x in segments]
        self._segment_connections = self._generate_segment_connections(segments)
        self._on_triggered_callback = None
        self._on_idle_triggered_callback = None

    def _generate_segment_connections(self, segments):
        connections = ['Idle'] + map(lambda x: x._name, segments) + ['Idle']
        segment_connections = []
        for x in xrange(len(connections) - 1):
            segment_connections.append({
                'From': connections[x],
                'To': connections[x+1] if x != 0 else '{}, {}'.format(connections[x], connections[x+1])
            })
        return segment_connections

    def on_triggered(self, callback):
        self._on_triggered_callback = callback

    def on_idle_triggered(self, callback):
        self._on_idle_triggered_callback = callback

    def add_sub_path(self, *gesture_segments):
        assert len(gesture_segments) >= 2, 'add_sub_path should accept at least two gesture segments'
        current_segments = map(lambda x: x._name, self._segments)
        # Add segments
        for x in xrange(len(gesture_segments) - 1):
           segment = gesture_segments[x]
           if segment._name not in current_segments:
               self._segments.append(segment) 
        # Add connections
        for x in xrange(len(gesture_segments) - 1):
            from_, to_ = gesture_segments[x]._name, gesture_segments[x+1]._name
            current_from_connections = map(lambda x: x['From'], self._segment_connections)
            if not from_ in current_from_connections:
                self._segment_connections.append({'From': from_, 'To': to_})
            else:
                current_connection = filter(lambda x: x['From'] == from_, self._segment_connections)[0]
                current_connection['To'] += ', {}'.format(to_)