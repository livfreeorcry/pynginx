import socket
import json

def lookup(address):
	"""
	reverse lookup to get hostname for nagios
	needs IPv4 address (also happy with hostname...but then it just returns what you put in)
	will accept IP with port (eg 10.10.10.10:1010)
	returns hostname, strips rest of FQDN (eg returns 'song' from 'song.quotemedia.com')
	"""
	ip=address.split(':')[0]
	try:
		hostname=socket.gethostbyaddr(ip)[0].split('.')[0]
	except socket.herror:
		print "Unkown host"
		return ip
	except socket.gaierror as g:
		print "Bad input. ", g
	else:
		return hostname

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
		ip=self.ip(address)
		try:
			hostname=socket.gethostbyaddr(ip)[0].split('.')[0]
		except socket.herror:
			print "Unkown host"
			return ip
		except socket.gaierror as g:
			print "Bad input. ", g
		else:
			return hostname

	def ip(self, ip):
		return ip.split(':')[0]