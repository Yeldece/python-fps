class Logger(object):
	def __init__(self):
		self.entries=[]
	
	def reset(self):
		self.entries=[]
	
	
	def add_entry(self, the_entry):
		self.entries.append(the_entry)
	
	def write(self, filename, should_reset=False):
		with open(filename, "a") as f:
			if len(self.entries) > 0:
				for i in self.entries:
					f.write(i+"\n")
			if should_reset:
				self.reset()