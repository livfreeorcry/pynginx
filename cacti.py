from sys import stdout
def cacti(blob, names, subcommand, logfile):
	if len(subcommand)<2: 
		subcommand=['cacti','index']
	if subcommand[1]=='index': 
		for line in cactiIndex(blob): 
			print line
			with open(logfile, "a") as log:
				log.write(line+"\n")
	elif subcommand[1]=='count':
		count = 0
		for line in cactiIndex(blob):
			count += 1
		print count
	elif subcommand[1]=='query': 
		for line in cactiQuery(blob, subcommand[2], names): 
			print line
			with open(logfile, "a") as log:
				log.write(line+"\n")
	elif subcommand[1]=='get':
		stdout.write( str(cactiGet(blob, subcommand[2], subcommand[3])) )
		with open(logfile, "a") as log:
				log.write(str(cactiGet(blob, subcommand[2], subcommand[3]))+"\n")
	else: 
		print "Unrecognized command: {0}".format(subcommand[1])
		with open(logfile, "a") as log:
				log.write("Unrecognized command: {0}\n".format(subcommand[1]))

def cactiIndex(blob):
	results=[]
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			results.append(instance["server"])
	return results

def cactiQuery(blob, query, names):
	results=[]
	if query == 'upstream':
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], upstream]))
	elif query == 'hostname':
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], names.lookup(instance["server"])]))
	else:
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], str(instance[query])]))
	return results

def cactiGet(blob, query, index):
	index=str(index)
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			if instance["server"]==index:
				return instance[query]
	return None
	
