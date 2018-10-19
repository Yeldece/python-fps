import time
class timer(object):
	def __init__(self):
		self.inittime=int(time.time() * 1000)

	def elapsed(self):
		return int(time.time() * 1000)-self.inittime

	def restart(self):
		self.inittime=int(time.time() * 1000)