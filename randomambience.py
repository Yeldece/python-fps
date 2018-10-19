import random
import globals as g
class RandomAmbience:
	def __init__(self, x, y, z, soundlist, time, referencedistance=1, rollofffactor=1):
		self.x=x
		self.y=y
		self.z=z
		self.soundlist=soundlist
		self.reference_distance=referencedistance
		self.rolloff_factor=rollofffactor
		self.timer=g.timer.timer()
		self.time=time
	
	def update(self):
		if self.timer.elapsed()>=self.time:
			self.timer.restart()
			if len(self.soundlist) > 0:
				rnd=random.randint(0, (len(self.soundlist)-1))
				ambsound=g.oalOpen(self.soundlist[rnd])
				ambsound.set_position((self.x, self.z, self.y))
				ambsound.set_reference_distance(self.reference_distance)
				ambsound.set_rolloff_factor(self.rolloff_factor)
				g.sourcelist.append(ambsound)
				ambsound.play()