from math import ceil, floor
import console
import os
import map
import doors
import movement
import wx
import random
app=wx.App()
import globals as g
import pyglet
from pyglet.window import key
import time
from AGK.mainframe import timer
from AGK.speech import auto
from openal import *
g.main_menu()
window=pyglet.window.Window(1366, 768, resizable=False, fullscreen=True, caption="FPS thing")
window.clear()
app.MainLoop()
def mainloop(	dt):
	try:
		draw()
		g.cleanup()
		if g.menulist!=g.mainmenu:
			for r in map.randomambs:
				r.update()
			if map.myroom()!="" and map.myroom() != g.currentroom:
				g.currentroom=map.myroom()
				if g.roomsound.get_state()==al.AL_PLAYING:
					g.roomsound.stop()
				g.roomsound=g.oalOpen(map.myroom(), ".wav")
				g.roomsound.set_looping(True)
				g.roomsound.play()
	
	
			if g.jumping == 1:
				g.WalkTime=g.airtime
				if g.ascending==True:
					if map.tile(g.me.x, g.me.y, g.me.z+1) == "":
						if g.jumptime.elapsed()>=50:
							g.jumptime.restart()
							g.ascenddistance+=1
							g.me.z+=1
							g.checkplatform()
					elif map.tile(g.me.x, g.me.y, g.me.z+1) != "":
						g.checkplatform()
						g.ascenddistance=0
						if map.mytile()=="":
							g.falling=1
						g.descenddistance=0
						g.jumping=0
					if g.ascenddistance > 5:
						g.ascending=False
				elif g.ascending == False:
					if g.jumptime.elapsed() >= 70:
						g.jumptime.restart()
						g.descenddistance+=1
						g.me.z-=1
						g.checkplatform()
					if g.descenddistance > 15:
						g.ascenddistance=0
						g.descenddistance=0
						g.jumping = 0
			g.falldown()
			if g.loaded and g.falling==0 and g.jumping==0 and map.tile(g.me.x, g.me.y, g.me.z) == "":
				g.falling=1
				
			if g.falling==1 and map.tile(g.me.x, g.me.y, g.me.z) != "":
				g.WalkTime=g.MainWalkTime
				if g.falldistance>10:
					tempsplit=map.mytile().split("|")
					fallingsounds=list()
					for x in tempsplit:
						fallingsounds.append("sounds/footsteps/"+x+"/falling/"+str(random.randint(1, len(g.find_files("sounds/footsteps/"+x+"/falling"))))+".wav")
					for x in fallingsounds:
						fallsound=g.oalOpen(x, ".wav")
						fallsound.set_source_relative(True)
						g.sourcelist.append(fallsound)
						fallsound.play()
				elif g.falldistance <= 10:
					if "wall" not in map.tile(g.me.x, g.me.y, g.me.z):
						tempsplit=map.mytile().split("|")
						landingsounds=list()
						for x in tempsplit:
							landingsounds.append("sounds/footsteps/"+x+"/landing/"+str(random.randint(1, len(g.find_files("sounds/footsteps/"+x+"/landing"))))+".wav")
						for x in landingsounds:
							landsound=g.oalOpen(x, ".wav")
							landsound.set_source_relative(True)
							g.sourcelist.append(landsound)
							landsound.play()
				g.fallingwind.stop()
				g.fallingwind.set_gain(0.01)
				g.jumping=0
				g.falling=0
				g.falldistance=0
		if g.menu==False and g.connecting==False:
			if "LSHIFT" in g.input or "RSHIFT" in g.input:
				if g.WalkTime > g.airtime:
					g.WalkTime=27
			if g.turntime.elapsed() >= 5:
				if "LALT" not in g.input and "RALT" not in g.input:
					if "Q" in g.input:
						g.turntime.restart()
						g.direction=movement.turnleft(g.direction, 1)
					elif "E" in g.input:
						g.turntime.restart()
						g.direction=movement.turnright(g.direction, 1)
			if g.walktimer.elapsed()>=180:
				if "PAGEUP" in g.input and map.tile(g.me.x, g.me.y, g.me.z+1)!="wall" and map.tile(g.me.x, g.me.y, g.me.z+1)!="" and g.jumping==0:
					g.walktimer.restart()
					tempsplit=map.mytile().split("|")
					stepsounds=list()
					for x in tempsplit:
						stepsounds.append(g.oalOpen("sounds/footsteps/"+x+"/"+str(random.randint(1, len(g.find_files("sounds/footsteps/"+x))))+".wav", ".wav"))
					for stepsound in stepsounds:
						stepsound.set_source_relative(True)
						g.sourcelist.append(stepsound)
						stepsound.play()
					g.me.z+=1
					if "wall" in map.tile(g.me.x, g.me.y, g.me.z+1):
						wallsound=g.oalOpen("sounds/wall.wav")
						wallsound.set_source_relative(True)
						g.sourcelist.append(wallsound)
						wallsound.play()
				if "PAGEDOWN" in g.input and map.tile(g.me.x, g.me.y, g.me.z-1)!="wall" and map.tile(g.me.x, g.me.y, g.me.z-1)!="" and g.jumping==0:
					g.walktimer.restart()
					tempsplit=map.mytile().split("|")
					stepsounds=list()
					for x in tempsplit:
						stepsounds.append(g.oalOpen("sounds/footsteps/"+x+"/"+str(random.randint(1, len(g.find_files("sounds/footsteps/"+x))))+".wav", ".wav"))
					for stepsound in stepsounds:
						stepsound.set_source_relative(True)
						g.sourcelist.append(stepsound)
						stepsound.play()
					g.me.z-=1
					if "wall" in map.tile(g.me.x, g.me.y, g.me.z-1):
						wallsound=g.oalOpen("sounds/wall.wav")
						wallsound.set_source_relative(True)
						g.sourcelist.append(wallsound)
						wallsound.play()

			if g.walktimer.elapsed()>=g.WalkTime:
				if "W" in g.input:
					g.walktimer.restart()
					movement.move(g.direction, 0.1)
					if g.ascenddistance > 0:
						g.checkplatform()
				elif "S" in g.input:
					g.walktimer.restart()
					movement.move(movement.turnleft(g.direction, 180), 0.1)
					if g.ascenddistance > 0:
						g.checkplatform()
				elif "A" in g.input:
					g.walktimer.restart()
					movement.move(movement.turnleft(g.direction, 90), 0.1)
					if g.ascenddistance > 0:
						g.checkplatform()
				elif "D" in g.input:
					g.walktimer.restart()
					movement.move(movement.turnright(g.direction, 90), 0.1)
					if g.ascenddistance > 0:
						g.checkplatform()



		g.listener.set_position((g.me.x, g.me.z, g.me.y))
		g.listener.set_orientation((movement.getpointer()[0], 0, movement.getpointer()[1], 0, 1, 0))
	except Exception as e:
		g.log_add_entry("\r\n"+str(e), True)
@window.event
def draw():
	window.clear()
@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.ESCAPE:
		try:
			if g.menu==False:
				g.main_menu()
			if g.menu == True and g.can_press_escape:
				g.menulist=list()
				g.menu=False
				g.menupos=-1
		except Exception as e:
			g.log_add_entry("\r\n"+str(e), True)
	try:
		if g.menu and g.connecting==False:
			if symbol == key.UP and g.menupos>0:
				if len(g.menulist) > 0:
					g.menupos-=1
					clicksound=g.oalOpen("sounds/relative/menumove.wav")
					g.sourcelist.append(clicksound)
					clicksound.play()
					g.speak(_(g.menulist[g.menupos]))
				else:
					g.speak(_("No menu item"))
			if symbol == key.DOWN and g.menupos<len(g.menulist)-1:
				if len(g.menulist) > 0:
					g.menupos+=1
					clicksound=g.oalOpen("sounds/relative/menumove.wav")
					g.sourcelist.append(clicksound)
					clicksound.play()
					g.speak(_(g.menulist[g.menupos]))
				else:
					g.speak(_("no menu item"))
			if symbol == key.ENTER and g.menupos>-1:
				if len(g.menulist) > 0:
					entersound=g.oalOpen("sounds/relative/menuselect.wav")
					g.sourcelist.append(entersound)
					entersound.play()
					g.perform_action(g.menulist[g.menupos])
				else:
					g.speak(_("no menu item"))
		if g.menu==False and g.connecting==False:
			if symbol == key.C:
				g.speak(str(g.me.x)+", "+str(g.me.y)+", "+str(g.me.z))
			if symbol==key.SLASH:
				data=""
				with open("maps/"+g.mapname+".map", "r") as f:
					data=g.getinput("map editor", "Enter map data here", True, f.read())
				if data != "":
					with open("maps/"+g.mapname+".map", "w") as f:
						f.write(data)
					map.door=list()
					map.tiles={}
					map.rooms={}
					map.consoles=list()
					map.randomambs=list()
					g.speak(_("Done"))
					map.parsedata(g.mapname)
					g.speak(_(g.mapname))
				else:
					g.speak(_("Failed editing map, Empty data passed"))

			if symbol == key.W or symbol == key.A or symbol == key.D or symbol == key.S:
				if map.mytile() != "":
					tempsplit=map.mytile().split("|")
					stepsounds=list()
					for x in tempsplit:
						if os.path.isdir("sounds/footsteps/"+map.mytile()+"/slow"):
							stepstr="sounds/footsteps/"+x+"/slow/"+str(random.randint(1, len(g.find_files("sounds/footsteps/"+x+"/slow"))))+".wav"
							if os.path.isfile(stepstr):
								stepsounds.append(g.oalOpen(stepstr))
					if len(stepsounds) > 0:
						for stepsound in stepsounds:
							stepsound.set_source_relative(True)
							g.sourcelist.append(stepsound)
							stepsound.play()
			if symbol==key.SPACE and g.jumping==0 and g.loaded and g.falling==0 and map.tile(g.me.x, g.me.y, g.me.z)!="":
				g.jumping=1
				g.ascending=True
				jumpingsound=g.oalOpen("sounds/jump.wav", ".wav")
				jumpingsound.set_source_relative(True)
				jumpingsound.play()
			if "LALT" in g.input or "RALT" in g.input:
				if symbol == key.Q:
					g.direction = movement.turnleft(g.direction, 45)
					g.speak(_("{0} degrees").format(g.direction))
				elif symbol == key.E:
					g.direction = movement.turnright(g.direction, 45)
					g.speak(_("{0} degrees").format(g.direction))
			if symbol == key.N:
				navigation=list()
				for m in map.door:
					if m.z==int(g.me.z) and movement.get_distance(int(g.me.x),int(g.me.y),int(g.me.z),m.x,m.y,m.z)<=50:
						navigation.append(_("door")+_(" is {0}, at coordinates {1}, {2}, {3}").format(movement.angle_to_string(g.direction, movement.calculate_angle(g.me.x, g.me.y, m.x, m.y, g.direction)), m.x, m.y, m.z))
				for m in map.consoles:
					if m.z==int(g.me.z) and movement.get_distance(int(g.me.x),int(g.me.y),int(g.me.z),m.x,m.y,m.z)<=50:
						navigation.append(_(m.name)+_(" is {0}, at coordinates {1}, {2}, {3}").format(angle_to_string(g.direction, calculate_angle(g.me.x, g.me.y, m.x, m.y, g.direction)), m.x, m.y, m.z))
				if len(navigation) > 0:
					g.menulist=navigation
					g.can_press_escape=True
					g.menu=True
					g.menupos=-1
					g.speak(_("Navigation menu: consists of {0} items").format(len(navigation)))
				else:
					g.speak(_("there is nothing here"))
			if symbol == key.P:
				g.speak(str(movement.calculate_angle(g.me.x, g.me.y, 2, 1, g.direction)))
			if symbol == key.ENTER:
				for m in map.consoles:
					if int(g.me.z)==m.z and movement.get_distance(int(g.me.x),int(g.me.y),int(g.me.z),m.x,m.y,m.z)==0:
						m.use()
				for m in map.door:
					if int(g.me.z)==m.z and movement.get_distance(int(g.me.x),int(g.me.y),int(g.me.z),m.x,m.y,m.z)==1:
						if m.open:
							closesound=g.oalOpen(m.closesound)
							g.sourcelist.append(closesound)
							closesound.set_position((m.x,m.z,m.y))
							closesound.play()
							m.open=False
						elif m.open==False:
							opensound=g.oalOpen(m.opensound)
							g.sourcelist.append(opensound)
							opensound.set_position((m.x,m.z,m.y))
							opensound.play()
							m.open=True
						
	except Exception as e:
		g.log_add_entry("\r\n"+str(e), True)
	g.input.append(key.symbol_string(symbol))
@window.event
def on_key_release(symbol, modifiers):
	if symbol==key.LSHIFT or symbol==key.RSHIFT:
		g.WalkTime=g.MainWalkTime
	if symbol == key.W or symbol == key.D or symbol == key.S or symbol == key.A:
		if g.step > 0.0 and g.step <=0.5:
			if g.step >= 0.3:
				stepback=g.oalOpen("sounds/footsteps/movement/stepback"+str(random.randint(1,6))+".wav")
				stepback.set_source_relative(True)
				g.sourcelist.append(stepback)
				stepback.play()
			g.step=0.0
			if symbol == key.A:
				g.me.x=ceil(g.me.x)
			elif symbol == key.D:
				g.me.x=floor(g.me.x)
			elif symbol == key.S:
				g.me.y=ceil(g.me.y)
			elif symbol == key.W:
				g.me.y=floor(g.me.y)
		
	if key.symbol_string(symbol) in g.input:
		g.input.remove(key.symbol_string(symbol))
pyglet.clock.schedule_interval(mainloop, 1/120.0)

pyglet.app.run()
