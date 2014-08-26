import socket
import os
import json
import sys

class Lookup():
	"""DNS lookup and (slow) cache
	Reverse-lookup for for nginx/nagios cross talk.

	Args:
		file (str):
			Name of the file used for storing dns responses.

	"""
	def __init__(self, dnsfile):
		self.dnsfile = dnsfile
		self.names = self.readDNS(dnsfile)

	def readDNS(self, dnsfile):
		if os.path.isfile(dnsfile):
			with open(dnsfile, 'r+') as file:
				try:
					return json.load(file)
				except ValueError as v:
					return dict()

	def writeDNS(self):
		with open(self.dnsfile, 'w') as file:
			file.write(str(self.names))
	
	def lookup(self, address):
		"""Return hostname of host at address.
		Returns address if dns doesn't respond.
		"""
		ip=self.ip(address)
		try:
			hostname=socket.gethostbyaddr(ip)[0].split('.')[0]
		except socket.herror:
			self.names[ip]="Unkown host"
			return ip
		else:
			self.names[ip]=hostname
			return hostname

	def ip(self, ip):
		return str(ip.split(':')[0])