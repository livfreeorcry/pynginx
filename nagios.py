import sys
from lookup import lookup
def nagios(blob, subcommand, env=None):
	"""Processes commands to return data in nagios's format.
	"""

	if (len(subcommand)<2) or (subcommand[1]=='check') : #Deafult to this if too few arguments provided
                response, exitCode = nagiosCheckLB(blob, env)
        else: 
                response= "Unrecognized command: {0}".format(subcommand[1])
                exitCode=3
        if exitCode==0: serviceState = "OK"
        elif exitCode==1: serviceState = "WARNING"
        elif exitCode==2: serviceState = "CRITICAL"
        else: serviceState="UNKNOWN"
        print "{0} {1}".format(serviceState, ", ".join(response))
        sys.exit(exitCode)

def nagiosCheckLB(blob, env=None):
        results=[]
        code=0
        okStates=["up"]
        criticalStates=["down","unavail","unhealthy"]
        warningStates=["warning"]
        for upstream in blob["upstreams"]:
                for instance in blob["upstreams"][upstream]:
                        if instance["state"] in okStates: pass
                        elif (instance["state"] in warningStates) & (code != 2): 
                                code=1
                                results.append(" - ".join([
                                        upstream,
                                        lookup(instance["server"], env), #gets the hostname
                                        instance["state"],
                                        ]))
                        elif instance["state"] in criticalStates: 
                                code=2
                                results.append(" - ".join([
                                        upstream,
                                        lookup(instance["server"], env), #gets the hostname
                                        instance["state"],
                                        ]))
                        elif (code!=2) | (code!=1) : 
                                code=3
                                results.append(" - ".join([
                                        upstream,
                                        lookup(instance["server"], env), #gets the hostname
                                        instance["state"],
                                        ]))                  
        return results, code
