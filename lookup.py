import socket

def lookup(address, env=False):
	"""Return hostname of host at address.
	Returns address if dns doesn't respond.
	"""
	ipaddress=ip(address, env)
	try:
		hostname=socket.gethostbyaddr(ipaddress)[0].split('.')[0]
	except socket.herror:
		return ipaddress
	else:
		return hostname

def ip(address, env=False):
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