from sys import stdout
from lookup import lookup
def cacti(blob, subcommand, env):
	"""Processes commands to return data in cacti's format.
	"""
	if len(subcommand)<2: #Default to providing an index if too few inputs are provided.
		subcommand=['cacti','index']
	if subcommand[1]=='index': 
		for line in cactiIndex(blob): 
			print line
	elif subcommand[1]=='count':
		print len(cactiIndex(blob))
	elif subcommand[1]=='query': 
		for line in cactiQuery(blob, subcommand[2], env): 
			print line
	elif subcommand[1]=='get':
		stdout.write( str(cactiGet(blob, subcommand[2], subcommand[3], env)) )
	elif subcommand[1]=='connections' or subcommand[1]=='requests':
		for L in blob[subcommand[1]]: 
			stdout.write(
		 		":".join( [str(L), str(blob[subcommand[1]][L])]) + " "
			)
	else: 
		print "Unrecognized command: {0}".format(subcommand[1])

def cactiIndex(blob):
	"""Returns a list of backends for cacti.
	These will be ip:port, one per line.
	These must be unique for cacti"""
	results=[]
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			results.append(instance["server"])
	return results

def cactiQuery(blob, query, env):

	results=[]
	if query == 'upstream':
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], upstream]))
	elif query == 'hostname':
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], lookup(instance["server"], env)]))
	else:
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], str(instance[query])]))
	return results

def cactiGet(blob, query, index, env):
	index=str(index)
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			if instance["server"]==index:
				if query == "hostname":
					return lookup(instance["server"], env)
				return instance[query]
	return None
