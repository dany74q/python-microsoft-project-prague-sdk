SEPERATOR = '\b'

def dict_to_string(dict_):
	res = ''
	for k, v in dict_.iteritems():
		if res:
			res += SEPERATOR
		res += '{key}{sep}{val}'.format(key=k, sep=SEPERATOR, val=v)
	return res + '\r\n'