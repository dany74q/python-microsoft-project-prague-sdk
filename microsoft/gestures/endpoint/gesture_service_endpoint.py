from microsoft.gestures.protocol.serialization_utils import dict_to_string
from microsoft.gestures.gesture_container import GestureContainer
from microsoft.gestures.protocol.client_info import ClientInfo
from microsoft.gestures.version import API_VERSION
from microsoft.gestures.logging import get_logger
from socket import create_connection
from psutil import process_iter
from select import select
import logging
import os


class GestureServiceEndpoint(object):
	SKELETON_SEPERATOR = '|'
	SEGMENT_SEPERATOR = '\\'
	ENCODING = '\xef\xbb\xbf'
	logger = get_logger('GestureServiceEndpoint')

	def __init__(self, protocol, host, port):
		self._socket = self._create_connection(host, port)
		self._protocol = protocol
		# Send BOM encoding after connection
		self._socket.sendall(self.ENCODING)
		self._pid = None
		self._process_name = None
		self._on_status_changed = lambda x: None
		self._registered_gestures = []

	def connect(self):
		self._pid, self._process_name = self.get_process_info()
		client_info = self.get_client_info(self._process_name, self._pid, API_VERSION)

		self.send_client_info(client_info)
		self.send_workflow_registration()
		if self._on_status_changed:
			self._on_status_changed(EndpointStatus('Connected'))

	def register_gesture(self, gesture, is_global=False):
		gesture_container = GestureContainer(gesture, is_global, self._pid)
		self._registered_gestures.append(gesture)
		self._send_registration(gesture_container)
		res = self._socket.recv(1024)
		self.verify_server_responce(res)

	def on_status_changed(self, callback):
		self._on_status_changed = callback

	def _send_registration(self, gesture_container):
		request = self._protocol.create_register_gesture_message(self.serialize_gesture(gesture_container), gesture_container._is_global, gesture_container._pid)
		self.send(request)

	def serialize_gesture(self, gesture_container):
		return gesture_container.to_xaml().replace('\r\n', '')

	def get_client_info(self, process_name, pid, api_version):
		self.logger.info('Getting client info')
		client_info = ClientInfo(process_name, pid, api_version)
		self.logger.info('Got client info - {}'.format(client_info))
		return client_info

	def get_process_info(self):
		self.logger.info('Getting pid, process name')
		pid = os.getpid()
		process_name = [p.name() for p in process_iter() if p.pid == pid]
		assert process_name, 'Could not find process with pid = {}'.format(pid)
		process_name = process_name[0]
		self.logger.info('Got pid = {}; process name = {}'.format(pid, process_name))
		return pid, process_name

	def _create_connection(self, host, port):
		self.logger.info('Creating connection to {}:{}'.format(host, port))
		return create_connection((host, port))

	def send(self, gestures_request):
		gestures_str = dict_to_string(gestures_request.message)
		self.logger.info('Sending msg - {}'.format(gestures_str))
		self._socket.sendall(gestures_str)

	def send_client_info(self, client_info):
		self.logger.info('Sending client info - {}'.format(client_info))
		req = self._protocol.create_client_info_message(client_info)
		self.logger.info('Sending client info msg - {}'.format(req))
		self.send(req)

	def poll(self):
		self._on_status_changed(EndpointStatus('Detecting'))
		while True:
			ready_to_read, ready_to_write, in_error = select((self._socket,), (), (), 1)
			if ready_to_read:
				buff = self._socket.recv(8192)
				for registered_gesture in self._registered_gestures:
					gesture_was_triggered = '{}{}'.format(self.SKELETON_SEPERATOR, registered_gesture._name) in buff
					if gesture_was_triggered:
						registered_gesture._on_triggered_callback()
					for segment in registered_gesture._segments:
						segment_was_triggered = '{}{}'.format(self.SEGMENT_SEPERATOR, segment._name) in buff
						if segment_was_triggered and segment._on_triggered:
							segment._on_triggered()
					idle_was_triggered = '{}{}'.format(self.SEGMENT_SEPERATOR, 'Idle') in buff
					if idle_was_triggered and registered_gesture._on_idle_triggered_callback:
						registered_gesture._on_idle_triggered_callback()

	def send_workflow_registration(self):
		request = self._protocol.create_register_to_workflow_message()
		self.send(request)
		res = self._socket.recv(4096)
		self.verify_server_responce(res)
		return res


	def verify_server_responce(self, response):
		self.logger.info('Verifying gesture server responce')
		assert 'exception' not in response.lower(), 'Gesture response error - {}'.format(response)
		self.logger.info('Server response is OK - {}'.format(response))


class EndpointStatus(object):
	def __init__(self, status):
		self.status = status
