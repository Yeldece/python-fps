import random
import map
import globals as g
import math
import openal as al
class vector:
	def __init__(self, x=0, y=0, z=0):
		self.x=x
		self.y=y
		self.z=z
	
	def value(self):
		return (self.x, self.y, self.z)
		

def get_distance(x1, y1, z1, x2, y2, z2):
	x=abs(x1-x2)
	y=abs(y1-y2)
	z=abs(z1-z2)
	return math.sqrt(x*x+y*y+z*z)

def calculate_angle(x1, y1, x2, y2, deg):
	x1=int(x1)
	y1=int(y1)
	x2=int(x2)
	y2=int(y2)
	x=x2-x1
	y=y1-y2
	if x==0:
		x+=0.0000001
	if y == 0:
		y+=0.0000001
	rad=0
	arctan=0
	if x != 0 and y!= 0:
		rad=math.atan(y/x)
		arctan=rad/3.14*180
	fdeg=0
	if x >0:
		fdeg=360-arctan
	elif x < 0:
		fdeg=180-arctan
	if x ==0:
		if y > 0:
			fdeg = 180
		elif y < 0:
			fdeg=0
		elif y == 0:
			fdeg=0
	
	fdeg-=deg
	if fdeg < 0:
		fdeg+=360
	fdeg=round(fdeg, 0)
	if fdeg == 360:
		fdeg = 0
	return fdeg

def angle_to_string(dir, angle):
	angle=turnright(dir, angle)
	if angle == 270:
		return _("north")
	elif angle == 315:
		return _("northeast")
	elif angle == 0:
		return _("east")
	elif angle== 45:
		return _("southeast")
	elif angle == 90:
		return _("south")
	elif angle == 135:
		return _("southwest")
	elif angle == 180:
		return _("west")
	elif angle == 225:
		return _("northwest")
	if angle > 270 and angle < 315:
		return _("northnortheast") 
	elif angle > 315 and angle < 360:
		return _("east northeast")
	elif angle > 0 and angle < 45:
		return _("east southeast")
	elif angle > 45 and angle < 90:
		return _("south southeast")
	elif angle > 90 and angle < 135:
		return _("south southwest")
	elif angle > 135 and angle < 180:
		return _("west southwest")
	elif angle > 180 and angle < 225:
		return _("west northwest")
	elif angle > 225 and angle < 270:
		return _("north northwest")
	return ""
def turnleft(deg, inc):
	deg-=inc
	if deg < 0:
		deg+=360
	return deg

def turnright(deg, inc):
	deg+=inc
	if deg >= 360:
		deg-=360
	return deg

def move(theta, distance):
	g.step+=1
	tempa = g.me.x+(distance*math.cos((theta*3.14)/180))
	tempb=g.me.y+(distance*math.sin((theta*3.14)/180))
	tempa=round(tempa, 2)
	tempb=round(tempb, 2)
	temps=""
	if "%d:%d:%d"%(tempa, tempb, g.me.z) in map.tiles:
		temps=map.tiles["%d:%d:%d"%(tempa,tempb,g.me.z)]
	doorfound=False
	for m in map.door:
		if get_distance(int(tempa),int(tempb),int(g.me.z),m.x,m.y,m.z) == 0:
			if m.open==False:
				doorfound=True
				break
	if "wall" in temps or doorfound:
		if g.step >5:
			g.step=0
			wall=g.oalOpen("sounds/wall.wav", ".wav")
			wall.set_source_relative(True)
			g.sourcelist.append(wall)
			wall.play()
	elif "wall" not in temps and doorfound == False:
		g.me.x=tempa
		g.me.y=tempb
		if g.step >5:
			g.step=0
			if map.mytile() != "":
				tempsplit=temps.split("|")
				stepsounds=list()
				for x in tempsplit:
					stepsounds.append(g.oalOpen("sounds/footsteps/"+x+"/"+str(random.randint(1, len(g.find_files("sounds/footsteps/"+x))))+".wav", ".wav"))
				for stepsound in stepsounds:
					stepsound.set_source_relative(True)
					g.sourcelist.append(stepsound)
					stepsound.play()
		if map.myroom()!="" and map.myroom() != g.currentroom:
			g.currentroom=map.myroom()
			if g.roomsound.get_state()==al.AL_PLAYING:
				g.roomsound.stop()
			g.roomsound=g.oalOpen(map.myroom(), ".wav")
			g.roomsound.set_looping(True)
			g.roomsound.play()

def getpointer():
	tempa = 0+(1*math.cos((g.direction*3.14)/180))
	tempb=0+(1*math.sin((g.direction*3.14)/180))
	return (tempa, tempb)