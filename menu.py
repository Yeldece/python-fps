import globals as g
import sys
import time
from AGK.speech import auto
from openal import *
sourcelist=[]
def cleanup():
	try:
		for a in sourcelist:
			if a == None or a.get_state()==AL_STOPPED:
				a.destroy()
				sourcelist.remove(a)
	except Exception as e:
		auto.speak("\r\nError acurd on cleaning up sound sources: {0}".format(str(e)))

class Menu:
	def __init__(self, clicksound, edgesound, wrapsound, entersound, opensound, items, itempos=0, title="menu", fpscap=120):
		self.clicksound=clicksound
		self.edgesound=edgesound
		self.wrapsound=wrapsound
		self.entersound=entersound
		self.opensound=opensound
		self.itempos=itempos
		self.items=items
		auto.speak(title+". "+items[itempos])
#		self.clock=pygame.time.Clock()
		self.fpscap=fpscap
		
	
	def run(self):
		try:
			return self.loop()
		except Exception as e:
			auto.speak(str(e))
	def loop(self):
		while 1:
#		self.clock.tick(self.fpscap)
			cleanup()
			if 'ENTER' in g.input:
				source=oalopen(entersound)
				sourcelist.append(source)
				source.play()
				return self.items[self.itempos]
