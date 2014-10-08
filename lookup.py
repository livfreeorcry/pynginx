import socket

def lookup(address, env=False):
	"""Return hostname of host at given address.
	Returns address if dns doesn't respond.

	address: should be the host instance provided by nginx
	env: passed to ip() for environment specific teaks
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
	eg, 8.8.8.8:80 returns 8.8.8.8

	address should be the ip:port
	env flags some environment specific 
		changes, see below."""
	ip = str(address.split(':')[0])
	if env=='dev':
		#hackiness for environment specific silliness.
		#Changes ips, eg from 8.8.8.8 to 8.8.2.8
		ip=ip.split('.')
		ip[2]="2"
		ip=".".join(ip)
	elif env=='prod':
		ip=ip.split('.')
		ip[2]="1"
		ip=".".join(ip)
	return ip
