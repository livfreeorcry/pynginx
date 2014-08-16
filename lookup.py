import socket
import json

class Lookup():
	"""DNS lookup and (slow) cache
	Reverse-lookup for for nginx/nagios cross talk.

	Args:
		file (str):
			Name of the file used for storing dns responses.

	"""
	def __init__(self, dnsfile):
		pass
	
	def lookup(self, address):
		"""
		"""
		ip=self.ip(address)
		try:
			hostname=socket.gethostbyaddr(ip)[0].split('.')[0]
		except socket.herror:
			print "Unkown host"
			return ip
		else:
			return hostname

	def ip(self, ip):

		return ip.split(':')[0]