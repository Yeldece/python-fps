import randomambience
import configobj
import console
import doors
import globals as g
randomambs=list()
from AGK.speech import auto
tiles=dict()
rooms=dict()
door=list()
consoles=list()
def spawn_tile(minx, maxx, miny, maxy, minz, maxz, type):
	for x in range(minx,maxx+1):
		for y in range(miny,maxy-1, -1):
			for z in range(minz,maxz+1):
				tiles[str(x)+":"+str(y)+":"+str(z)]=type
def mytile():
	if "%d:%d:%d"%(int(g.me.x), int(g.me.y), int(g.me.z)) in tiles:
		
		temps=tiles["%d:%d:%d"%(int(g.me.x),int(g.me.y),int(g.me.z))]
		return temps
	return ''

def spawn_room(minx, maxx, miny, maxy, minz, maxz, sound):
	for x in range(minx,maxx+1):
		for y in range(miny,maxy-1, -1):
			for z in range(minz,maxz+1):
				rooms[str(x)+":"+str(y)+":"+str(z)]=sound
def myroom():
	if "%d:%d:%d"%(int(g.me.x), int(g.me.y), int(g.me.z)) in rooms:
		temps=rooms["%d:%d:%d"%(int(g.me.x),int(g.me.y),int(g.me.z))]
		return temps
	return ''
def tile(x, y, z):
	if "%d:%d:%d"%(int(x), int(y), int(z)) in tiles:
		temps=str(tiles["%d:%d:%d"%(int(x),int(y),int(z))])
		return temps
	return ''
def parsedata(mapname):
	config=None
	try:
		config=configobj.ConfigObj("maps/"+mapname+".map")
		for m in config:
			if m[0:7] == "console":
				x=int(config[m]["x"])
				y=int(config[m]["y"])
				z=int(config[m]["z"])
				name=config[m]["name"]
				stations=config[m]["stations"].split(",")
				consoles.append(console.console(x, y, z, name, stations))
			if m[0:4] == "door":
				x=int(config[m]["x"])
				y=int(config[m]["y"])
				z=int(config[m]["z"])
				opensound=config[m]["opensound"]
				closesound=config[m]["closesound"]
				door.append(doors.door(x, y, z, opensound, closesound))
			if m[0:4] == "wall":
				x=int(config[m]["x"])
				y=int(config[m]["y"])
				z=int(config[m]["z"])
				length=int(config[m]["length"])
				side=int(config[m]["side"])
				depth=int(config[m]["depth"])
				spawn_tile(x, (x+side-1), y, (y+-(length)+1), z, (z+depth), "wall")
			if m[0:9] == "randomamb":
				x=int(config[m]["x"])
				y=int(config[m]["y"])
				z=int(config[m]["z"])
				sp=config[m]["sounds"].split(",")
				time=int(config[m]["time"])
				reference_distance=1.0
				rolloff_factor=1.0
				if "reference_distance" in config[m]:
					reference_distance=float(config[m]["reference_distance"])
				if "rolloff_factor" in config[m]:
					rolloff_factor=float(config[m]["rolloff_factor"])
				randomambs.append(randomambience.RandomAmbience(x, y, z, sp, time, reference_distance, rolloff_factor))
			if m[0:4] == "room":
				roomx=int(config[m]["x"])
				roomy=int(config[m]["y"])
				roomz=int(config[m]["z"])
				roomsound=config[m]["sound"]
				roomtype=config[m]["type"]
				roomlengthx=int(config[m]["lengthx"])
				roomlengthy=int(config[m]["lengthy"])
				roomdepth=int(config[m]["depth"])
				if "description" in config[m]:
					roomdesc=config[m]["description"]
				spawn_room(roomx, (roomx+roomlengthx-1), roomy, (roomy+-(roomlengthy)+1), roomz, (roomz+roomdepth), roomsound)
				spawn_tile(roomx, (roomx+roomlengthx-1), roomy, (roomy+-(roomlengthy)+1), roomz, (roomz+roomdepth), roomtype)
		g.mapname=mapname
		g.loaded=True
	except Exception as e:
		g.log_add_entry("Error on parsing data: "+str(e), True)