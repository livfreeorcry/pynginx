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
                        if instance["state"] not in okStates:
                                results.append("  ".join([
                                        lookup(instance["server"], env), #gets the hostname
                                        upstream,
                                        instance["state"],
                                        ]))
                                if (instance["state"] in criticalStates): code = 2
                                elif (instance["state"] in warningStates) and (code != 2): code = 1
                                elif code == 0: code = 3
        return results, code
