import socket
import __main__ as main

def lookup(self, address, env=False):
	"""Return hostname of host at address.
	Returns address if dns doesn't respond.
	"""
	ip=ip(address, env)
	try:
		hostname=socket.gethostbyaddr(ip)[0].split('.')[0]
	except socket.herror:
		return ip
	else:
		return hostname

def ip(self, address, qm=False):
	"""Split the address from its port, since nginx passes
	it over together.
	We also have the option for some """
	ip = str(address.split(':')[0])
	if env=='dev':
		#hackiness for environment specific silliness.
		#Changes ips, eg from x.x.x.x to x.x.2.x
		ip=ip.split('.')
		ip[2]=2
		ip=(str(ip[0])+'.'+str(ip[1])+'.'+str(ip[2])+'.'+str(ip[3]))
	elif env=='prod':
		ip=ip.split('.')
		ip[2]=1
		ip=(str(ip[0])+'.'+str(ip[1])+'.'+str(ip[2])+'.'+str(ip[3]))
	return ip