import sys
from lookup import lookup
from re import match
def nagios(blob, subcommand, env=None):
	"""Processes commands to return data in nagios's format.
	"""

	if (len(subcommand)<2) or (subcommand[1]=='check') : #Deafult to this if too few arguments provided
                response, exitCode = nagiosCheckLB(blob, env)
                response = ", ".join(response)
        elif (subcommand[1]=='connections') and (len(subcommand)>=3):
                warn,crit = subcommand[2].split(':')
                response, exitCode = nagiosMaxConns(blob, int(warn), int(crit))
                response = ", ".join(response)
        else: 
                response= "Unrecognized command: {0}".format(subcommand[1])
                exitCode=3
        if exitCode==0: serviceState = "OK:"
        elif exitCode==1: serviceState = "WARNING:"
        elif exitCode==2: serviceState = "CRITICAL:"
        else: serviceState="UNKNOWN:"
        print "{0} {1}".format(serviceState, response)
        sys.exit(exitCode)

def nagiosMaxConns(blob, warn, crit):
        results=[]
        code=0
        for upstream in blob["upstreams"]:
                for instance in blob["upstreams"][upstream]:
                        try:
                                pct = (int(instance["active"]) * 100) / int(instance["max_conns"])
                                if pct > crit:
                                        code = 2
                                        results.append("  ".join([
                                                lookup(instance["server"], env), #gets the hostname
                                                upstream,
                                                instance["active"],
                                        ]))
                                elif pct > warn and code != 2:
                                        code = 1
                                        results.append("  ".join([
                                                lookup(instance["server"], env), #gets the hostname
                                                upstream,
                                                instance["active"],
                                        ]))
                        except:
                                pass
        return results, code

def nagiosCheckLB(blob, env=None):
        results=[]
        code=0
        okStates=["up"]
        criticalStates=["down","unavail","unhealthy"]
        warningStates=["warning"]
        for upstream in blob["upstreams"]:
                for instance in blob["upstreams"][upstream]:
                        if instance["state"] not in okStates:
                                results.append("  ".join([
                                        lookup(instance["server"], env), #gets the hostname
                                        upstream,
                                        instance["state"],
                                        ]))
                                if (instance["state"] in criticalStates): code = 2
                                elif (instance["state"] in warningStates) and (code != 2): code = 1
                                elif code == 0: code = 3
        if results==[]:
                results=["All hosts in up state"]                       
        return results, code
 
