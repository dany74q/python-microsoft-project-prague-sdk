from microsoft.gestures.endpoint.gesture_service_endpoint import GestureServiceEndpoint
from microsoft.gestures.protocol.gestures_protocol import GesturesProtocol
from microsoft.gestures.logging import get_logger


class GesturesServiceEndpointFactory(object):
	logger = get_logger('GesturesServiceEndpointFactory')

	@classmethod
	def create(cls, host='localhost', port=46215):
		protocol = GesturesProtocol(port)

		endpoint = GestureServiceEndpoint(protocol, host, port)
		return endpoint
