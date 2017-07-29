class ClientInfo(object):
	SEPERATOR = ','

	def __init__(self, process_name, pid, api_version, seperator=SEPERATOR):
		self.process_name = process_name
		self.pid = pid
		self.api_version = api_version
		self.seperator = seperator

	def __str__(self):
		return '[{name}{sep}{pid}{sep}{api_ver}]'.format(
			name=self.process_name, sep=self.seperator, pid=self.pid, api_ver=self.api_version)
