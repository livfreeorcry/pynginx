import os
import __main__ as main

class Lock:
	"""Lockfile
Manages lock file to avoid running multiple instances of the script.

Args:
	lock (str, optional): Set the filename for the lock file. Defaults to the main filename.

	"""
	def __init__(self, lock=str(os.path.basename(main.__file__))+".lock"):
		self.lock=lock

	def create(self):
		"""Creates a lockfile with the name of the main python script. Checks for existing lock before creating.
		Returns:
			True if sucessful, Flase otherwise.
		"""
		if self.check():
			with open(self.lock, 'w') as file:
				file.write(str(os.getpid()))
				print "Creating lockfile"
				return True
		else: return False

	def check(self):
		"""Checks if the lockfile exits
		Returns:
			True if process is unlocked (no lock, or stale lock), false otherwise.
		"""
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
		"""Destroy lockfile
		Returns: 
			True if successful. Dies otherwise.
		"""
		try:
			os.remove(self.lock)
		except:
			print "Failed to remove lockfile, dying."
			exit(1)
		else:
			print "Removed lockfile."
			return True