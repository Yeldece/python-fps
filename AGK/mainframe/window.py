from attr import attrs, attrib, Factory
import pygame
pygame.init()
pygame.display.init()
@attrs
class window(object):
	title = attrib()
	width = attrib(default=Factory(lambda: 750))
	height = attrib(default=Factory(lambda: 750))

	def __attrs_post_init__(self):
		pygame.event.set_grab(True)
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.title)

	def show(self):
		#show the window
		pygame.display.flip()

