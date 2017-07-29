from microsoft.gestures.protocol.serialization_utils import dict_to_string
from microsoft.gestures.protocol.gestures_request import GesturesRequest
from microsoft.gestures.protocol.client_command import ClientCommand
from collections import OrderedDict


class GesturesProtocol(object):
	def __init__(self, port):
		self.port = port

	def create_register_to_workflow_message(self):
		return self.create_message(ClientCommand.RegisterToWorkflow)

	def create_unregister_from_workflow_message(self):
		return self.create_message(ClientCommand.UnregisterFromWorkflow)

	def create_client_info_message(self, client_info):
		return self.create_message(ClientCommand.SetClientInfo, ClientInfo=str(client_info))

	def create_register_gesture_message(self, gesture_str, is_global, pid):
		return self.create_message(ClientCommand.RegisterGesture, Gesture=gesture_str, IsGestureGlobal=str(is_global), ProcessId=str(pid))

	def create_message(self, command, **kwargs):
		d = OrderedDict()
		d['Command'] = command
		for k, v in kwargs.iteritems():
			if k and v:
				d[k] = v
		return GesturesRequest(d)