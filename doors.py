import globals as g
class door:
	def __init__(self, x, y, z, opensound, closesound):
		self.x=x
		self.y=y
		self.z=z
		self.opensound=opensound
		self.closesound=closesound
		self.open=False