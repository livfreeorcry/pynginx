#!/opt/python/bin/python
#a: James Burke
#e: jburke@quotemedia.com
#v: 0.3
from urllib2 import urlopen
from lock import Lock
import datetime
import socket
import json
import os

Timeout=10 		#Timeout for request to nginx status page
Nginx="http://10.2.2.1/status"
Nagios=None		#Nagios instance url

def main(nagios, url, timeout):
	lock=Lock()
	print lock.lock
	print "Checking for lockfile..."
	if lock.create():
		statusJson=json.loads(urlopen(url,timeout=timeout).read())
		for upstream in statusJson["upstreams"]:
			print upstream
			for instance in statusJson["upstreams"][upstream]:
				state=instance["state"]
				downtime=str(datetime.timedelta( seconds = (instance["downtime"]/1000)))
				host=lookup(instance["server"])
				print host + " - " + state + " - " + downtime
		lock.destroy()

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

main(Nagios, Nginx, Timeout)

