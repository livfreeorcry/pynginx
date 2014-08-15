import os
import __main__ as main

class Lock:
	"""
	Managing lock file to avoid running multiple simmultaneous requests to nginx
	"""
	#lock=str(os.path.basename(__file__))+".lock"
	lock=str(os.path.basename(main.__file__))+".lock"

	def create(self):
		if self.check():
			with open(self.lock, 'w') as file:
				file.write(str(os.getpid()))
				print "Creating lockfile"
				return True
		else: return False

	def check(self):
		if os.path.isfile(self.lock):
			with open(self.lock, 'r') as file:
				pid=file.readline()
				try:
				 os.kill(int(pid), 0)
				except OSError:
					print "Stale PID file, removing."
					self.destroy()
					return True
				else:
					print "Already running."
					return False
		else:
			return True 
	def destroy(self):
		try:
			os.remove(self.lock)
		except:
			print "Failed to remove lockfile, dying."
			exit(1)
		else:
			print "Removed lockfile."
			return True