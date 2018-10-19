import globals as g
class console:
	def __init__(self, x, y, z, name, stations):
		self.x=x
		self.y=y
		self.z=z
		self.name=name
		self.stations=stations
	
	def use(self):
		g.menulist=self.stations
		g.menupos=-1
		g.menu=True
		
	