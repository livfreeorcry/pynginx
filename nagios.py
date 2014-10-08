from sys import stdout
from lookup import lookup
def nagios(blob, env, subcommand):
	"""Processes commands to return data in nagios's format.
	"""
	if subcommand[1]=='check': 
		for line in nagiosCheck(blob, "state", env): 
			print line
	else: 
		print "Unrecognized command: {0}".format(subcommand[1])

def nagiosCheck(blob, query, env):

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
                                results.append("!".join([lookup(instance["server"], env), str(instance[query])]))
        return results
