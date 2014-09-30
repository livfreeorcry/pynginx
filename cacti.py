def cacti(blob, subcommand):
	if len(subcommand)<2: 
		subcommand=['cacti','index']
	if subcommand[1]=='index': 
		for line in cactiIndex(blob): print line
	elif subcommand[1]=='query': 
		for line in cactiQuery(blob, subcommand[2]): print line
	elif subcommand[1]=='get':
		print 'get'
	else: print "Unrecognized command: {0}".format(subcommand[1])
def cactiIndex(blob):
	results=[]
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			results.append(instance["server"])
	return results

def cactiQuery(blob, query):
	results=[]
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			results.append("!".join([instance["server"], str(instance[query])]))
	return results

def cactiGet(blob, query, index):
	results=[]
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			results.append("!".join([instance["server"], str(instance[query])]))
	return results