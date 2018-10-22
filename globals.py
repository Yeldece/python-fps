import gettext
langstring=""
try:
	with open("locale/savedlng", "r") as f:
		langstring=f.read()
except Exception as e:
	langstring="en"
lang=gettext.translation(langstring, localedir='locale', languages=[langstring])
lang.install()
import ast
#We use this module to evaluate strings as python expretions. At least for now
import random
import movement
import os
import map
import pyglet
from pyglet.window import key
import sys
import wx
import os
from logger import Logger
from AGK.speech import auto
from AGK.mainframe import timer
from openal import *
NICK=""
c=None
me=movement.vector(0, 0, 32)
class TextEntryDialog(wx.Dialog):
    def __init__(self, parent, title, caption):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(TextEntryDialog, self).__init__(parent, -1, title, style=style)
        text = wx.StaticText(self, -1, caption)
        input = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        input.SetInitialSize((400, 300))
        buttons = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL, 5)
        sizer.Add(buttons, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(input, 1, wx.EXPAND|wx.ALL, 5)
        input.SetFocus()
        self.SetSizerAndFit(sizer)
        self.input = input
    def SetValue(self, value):
        self.input.SetValue(value)
    def GetValue(self):
        return self.input.GetValue()
mapname=""
jumping=0
falling=0
falldamage=0
falldistance=0
ascenddistance=0
descenddistance=0
lastzone=""
zonestatus=1
zone=""
turntime=timer.timer()
falltime=timer.timer()
jumptime=timer.timer()
landtime=timer.timer()
fallingwind=oalOpen("sounds/misk/fallingwind.wav", ".wav")
fallingwind.set_source_relative(True)
fallingwind.set_gain(0.01)
fallingwind.set_looping(True)
WalkTime=40
MainWalkTime=40
airtime=10
ascending=False
loaded=False
walktimer=timer.timer()
roomsound=oalOpen("sounds/relative/room2.wav")
roomsound.set_looping(True)
currentroom=""
direction=270
listener=oalGetListener()
log=Logger()
sourcelist=[]
input=[]
connected=False
connecting=False
mainmenu=['play', 'change language', 'exit']
menupos=-1
menulist=[]
menu=False
menumusic=oalOpen("sounds/relative/menu.wav")
menumusic.set_looping(True)
menumusic.set_gain(0.3)
step=0
can_press_escape=False
def cleanup():
	try:
		for a in sourcelist:
			if a == None or a.get_state()==AL_STOPPED:
				a.destroy()
				sourcelist.remove(a)
	except Exception as e:
		log.add_entry("\r\nError acurd on cleaning up sound sources: {0}".format(str(e)))
def getinput(title, message, multiline=False, value=""):
	if multiline:
		input=TextEntryDialog(None, message, title)
	else:
		input=wx.TextEntryDialog(None, message, title)
	input.SetValue(value)
	input.ShowModal()
	text=input.GetValue()
	input.Destroy()
	return text
	

def reset():
	global mapname, currentroom, roomsound, jumping, falling, falldamage, ascenddistance, descenddistance, falldistance, lastzone, zonestatus, ascending, loaded, WalkTime, MainWalkTime, airtime, zone, me, direction
	mapname=""
	jumping=0
	falling=0
	falldamage=0
	falldistance=0
	ascenddistance=0
	descenddistance=0
	lastzone=""
	zonestatus=1
	zone=""
	fallingwind.set_source_relative(True)
	fallingwind.set_gain(0.01)
	fallingwind.set_looping(True)
	WalkTime=40
	MainWalkTime=40
	airtime=10
	ascending=False
	loaded=False
	walktimer=timer.timer()
	currentroom=""
	roomsound.stop()
	direction=270
	me=movement.vector(0, 0, 32)
	map.door=list()
	map.tiles={}
	map.rooms={}
	map.consoles=list()
	map.randomambs=list()

def main_menu():
	global menu, menulist, menupos, can_press_escape
	reset()
	menulist=['play', 'change language', 'exit']
	menupos=-1
	menu=True
	can_press_escape=False
	if menumusic.get_state() != AL_PLAYING:
		menumusic.play()
	auto.speak(_("Main menu. Select an item with up and down. Press enter to activate the item"))


def perform_action(what):
	global c, menu, menumusic, menulist, menupos, can_press_escape
	try:
		
		if what == 'play':
			map.parsedata("inderion station")
			menumusic.stop()
			menu=False
			menulist=list()
		elif what == 'change language':
			langlist=[]
			for x in find_dirs("locale"):
				langlist.append("language: "+x)
			langlist.append("exit to main menu")
			menulist=langlist
			menupos=-1
			speak(_("select a language"))
			menu=True
			can_press_escape=False
		elif what[0:10] == "language: ":
			language = what.replace("language: ", "")
			global lang
			lang=gettext.translation(language, localedir='locale', languages=[language])
			lang.install()
			auto.speak(_("language set to ")+_(language))
			with open("locale/savedlng", "w") as f:
				f.write(language)
			main_menu()
		elif what == "exit to main menu":
			main_menu()
		elif what == "exit":
			exit()
	except Exception as e:
		auto.speak(str(e))

def find_dirs(path):
	ourlist=[]
	for dir in os.listdir(path):
		if os.path.isdir(os.path.join(path, dir)):
			ourlist.append(dir)
	return ourlist

def find_files(path):
	ourlist=[]
	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path, file)):
			ourlist.append(file)
	return ourlist
def checkplatform():
	try:
		global jumping, WalkTime
		if map.tile(me.x, me.y, me.z) != "" and jumping == 1:
			if "wall" not in map.tile(me.x, me.y, me.z):
				tempsplit=map.mytile().split("|")
				landingsounds=list()
				for x in tempsplit:
					landingsounds.append("sounds/footsteps/"+x+"/landing/"+str(random.randint(1, len(find_files("sounds/footsteps/"+x+"/landing"))))+".wav")
				for x in landingsounds:
					landsound=oalOpen(x, ".wav")
					landsound.set_source_relative(True)
					sourcelist.append(landsound)
					landsound.play()

			jumping=0
			WalkTime=MainWalkTime
			global step
			step=0
			walktimer.restart()
			global ascenddistance, descenddistance
			ascenddistance=0
			descenddistance=0
	except Exception as e:
		auto.speak("\r\nError acurd on landing: {0}".format(str(e)))

def falldown():
	try:
		if falltime.elapsed()>=60 and falling==1:
			falltime.restart()
			me.z-=1
			global falldistance
			falldistance+=1
			if fallingwind.get_state() != AL_PLAYING:
				fallingwind.play()
			if fallingwind.gain<2.0:
				fallingwind.set_gain(fallingwind.gain+0.01)
	except Exception as e:
		auto.speak("\r\nError acurd while falling down: {0}".format(str(e)))

#This function just speaks a text. Maybe for easier writing...
def speak(text):
	try:
		auto.speak(text)
	except Exception as e:
		auto.speak("Error on speaking a text: "+str(e))

def exit():
	log.write("log.log")
	sys.exit()