import viz
import random
import viztask
import math

tracker = viz.add('intersense.dls')
viz.mouse.setVisible(viz.OFF)
viz.window.setFullscreen(viz.ON)
viz.window.setBorder( viz.BORDER_NONE )
viz.go()
viz.phys.enable()
#viz.disable( viz.LIGHTING )
light1 = viz.addLight()
light1.position(0,5,0)
light1.color(viz.WHITE)

#env = viz.add(viz.ENVIRONMENT_MAP, 'eucalyptus\eucalyptus.jpg',scene=viz.MainScene)
env = viz.add(viz.ENVIRONMENT_MAP, 'sky.jpg',scene=viz.MainScene)
sky = viz.add('skydome.dlc')
sky.texture(env)

TRANSLATE_INC = .2
ROTATION_INC = 2
SCALE = [0.03, 0.03, 0.03]
room = viz.add("../models/room2/room2.wrl")
room.setScale(SCALE)

vizact.whilekeydown(viz.KEY_UP,viz.move,0,0,TRANSLATE_INC) #Move forward while up key is pressed
vizact.whilekeydown(viz.KEY_DOWN,viz.move,0,0,-TRANSLATE_INC) #Move backward while down key is pressed
vizact.whilekeydown(viz.KEY_LEFT,viz.rotate,viz.BODY_ORI,-ROTATION_INC,0,0) #Turn left while left arrow pressed
vizact.whilekeydown(viz.KEY_RIGHT,viz.rotate,viz.BODY_ORI,ROTATION_INC,0,0) #Turn right while right arrow pressed

nfalsepos = 0
nfalseneg = 0
ncorrect = 0
tophatwindow = -1
tophatclicked = 0
def onclick():
	global tophatwindow,tophatclicked,nfalsepos,ncorrect
	if ( tophatwindow == -1 ):
		nfalsepos += 1
	elif ( tophatclicked == 0 ):
		ncorrect += 1
		tophatclicked = 1
	print [ncorrect, nfalsepos, nfalseneg]

#results_tbox = viz.addTextbox()
#results_tbox.setPosition(0.5,0.15)
#
#def updateResults():
#	global results_tbox,nfalsepos,nfalseneg,ncorrect
#	updateResults.message( str(ncorrect)+" "+str(nfalsepos)+" "+str(ncorrect))
#
#vizact.ontimer(0,updateResults)

vizact.onmousedown(viz.MOUSEBUTTON_LEFT,onclick)

HMDfov_vert = 36.
HMDwidth = 640.
HMDheight = 480.
HMDaspect = HMDwidth/HMDheight

viz.fov( HMDfov_vert, HMDaspect )
viz.window.setSize( HMDwidth, HMDheight )

ground = viz.add('tut_ground.wrl')
ground.setScale([5,1,5])
#viz.translate(viz.HEAD_POS,0,20,-20)
#viz.lookat(0,0,0)
viz.clearcolor(viz.SKYBLUE)

#window = viz.add(viz.WINDOW)
#window.setPosition(.5,.5)

node = viz.addRenderNode()
node.setScene( viz.Scene2 )
node.setBuffer( viz.RENDER_FRAME_BUFFER )
node.setOrder( viz.POST_RENDER )
node.setInheritView( 0 )
node.setClearMask( 0 )
node.disable( viz.DEPTH_TEST );

hmdview = 0
def setARfov( val ):
	global node, ARfov_vert, hmdview	
	ARfov_vert = val
	ARheight = HMDheight / HMDfov_vert * ARfov_vert
	ARwidth = ARheight * HMDaspect
	ARx = (HMDwidth - ARwidth)/2
	ARy = (HMDheight - ARheight)/2
	print ARwidth,ARheight,ARx,ARy
	node.setFov( ARfov_vert, HMDaspect, 0.1, 10 )
	node.setSize( ARwidth,ARheight,ARx,ARy )
	
	if(hmdview != 0):
		hmdview.remove()
	viz.startlayer(viz.QUADS)
	viz.vertex([ARx,ARy,0])
	viz.vertex([ARx + ARwidth, ARy,0])
	viz.vertex([ARx + ARwidth,ARy + ARheight,0])
	viz.vertex([ARx,ARy + ARheight,0])
	hmdview = viz.endlayer(viz.WORLD,viz.Scene3)
	hmdview.alpha(0.15)

setARfov( 20 )




node2D = viz.addRenderNode()
node2D.setScene(viz.Scene3)
node2D.setBuffer( viz.RENDER_FRAME_BUFFER )
node2D.setOrder( viz.POST_RENDER )
node2D.setInheritView(0)
node2D.setSize( HMDwidth,HMDheight )
node2D.setProjectionMatrix(viz.Matrix.ortho2D(0,HMDwidth,0,HMDheight))
node2D.setClearMask(0)
node2D.disable(viz.DEPTH_TEST)
#viz.startlayer(viz.LINES)
#viz.vertex([HMDwidth/2,0,0])
#viz.vertex([HMDwidth/2,HMDheight,0])
#viz.endlayer(viz.WORLD,viz.Scene3)









ringbuffer_len = 20
yaw_ringbuffer = range(ringbuffer_len)
pitch_ringbuffer = range(ringbuffer_len)
roll_ringbuffer = range(ringbuffer_len)
for i in range(ringbuffer_len):
	yaw_ringbuffer[i] = 0
	pitch_ringbuffer[i] = 0
	roll_ringbuffer[i] = 0
ringbuffer_idx = 0


def UpdateMovement():
	global tracker
	global node
	global yaw_ringbuffer, pitch_ringbuffer, roll_ringbuffer, ringbuffer_idx
	global ringbuffer_len
	
	yaw = yaw_ringbuffer[ringbuffer_idx]
	pitch = pitch_ringbuffer[ringbuffer_idx]
	roll = roll_ringbuffer[ringbuffer_idx]

	node.setPosition( viz.MainView.getPosition() )
	node.setEuler( yaw,pitch,roll )
	
	#Get tracker euler rotation
	yaw,pitch,roll = tracker.getEuler()
	viz.MainView.setEuler([yaw,pitch,roll])
	#yaw,pitch,roll = viz.MainView.getEuler()
	
	yaw_ringbuffer[ringbuffer_idx] = yaw
	pitch_ringbuffer[ringbuffer_idx] = pitch
	roll_ringbuffer[ringbuffer_idx] = roll
	
	ringbuffer_idx = (ringbuffer_idx + 1)%ringbuffer_len
	
vizact.ontimer(0,UpdateMovement)

#fovslider = viz.addSlider()
#fovslider.translate(0.2,0.1)
#fovslider.set(ARfov_vert/HMDfov_vert)

#def onButton(obj,state):
#	global fovslider, HMDfov_vert
#	if obj == fovslider:
#		setARfov( HMDfov_vert * fovslider.get() )
#
#viz.callback(viz.BUTTON_EVENT,onButton)



#Create custom camera handler
class MyCameraHandler( viz.CameraHandler ):
	a=0
#	def _camUpdate( self, e ):
#		if viz.iskeydown( viz.KEY_RIGHT ):
#			e.view.rotate(0,1,0,1,viz.BODY_ORI,viz.REL_PARENT)
#			#e.view2.rotate(0,1,0,1,viz.BODY_ORI,viz.REL_PARENT)
#		elif viz.iskeydown ( viz.KEY_LEFT ):
#			#move view up
#			e.view.rotate(0,1,0,-1,viz.BODY_ORI,viz.REL_PARENT)
#			#e.view2.rotate(0,1,0,-1,viz.BODY_ORI,viz.REL_PARENT)

viz.cam.setHandler( MyCameraHandler() )


num_av = 20
real_room_x = 8
room_x = real_room_x + 2
real_room_y = 6
room_y = real_room_y + 2
max_x = 25
max_y = 25
max_walk_x = max_x + 2
max_walk_y = max_y + 2

"""
viz.startlayer(viz.LINES) 
viz.vertex(-real_room_x,1,real_room_y) #Vertices are split into pairs.
viz.vertex(real_room_x,1,real_room_y)

viz.vertex(real_room_x,1,real_room_y)
viz.vertex(real_room_x,1,-real_room_y)

viz.vertex(real_room_x,1,-real_room_y)
viz.vertex(-real_room_x,1,-real_room_y)

viz.vertex(-real_room_x,1,-real_room_y)
viz.vertex(-real_room_x,1,real_room_y)
myLines = viz.endlayer()
"""



class quadrant:
	next_to = []
	
	def __init__(self, x1, x2, y1, y2):
		self.x1 = x1
		if x1 < 0:
			self.x1_walk = x1 + 2
		else:
			self.x1_walk = x1 + 2
			
		self.x2 = x2
		if x2 < 0:
			self.x2_walk = x2 - 2
		else:
			self.x2_walk = x2 - 2
			
		self.y1 = y1
		if y1 < 0:
			self.y1_walk = y1 + 2
		else:
			self.y1_walk = y1 + 2
			
		self.y2 = y2
		if y2 < 0:
			self.y2_walk = y2 - 2
		else:
			self.y2_walk = y2 - 2
	
	def contains(self, point):
		##print point
		#print [self.x1, self.x2]
		#print [self.y1, self.y2]
		if self.x1 <= point[0] and self.x2 > point[0]:
			if self.y1 <= point[2] and self.y2 > point[2]:
				return True
		return False
		
	def get_random_walk(self):
		return self.next_to[random.randrange(0, len(self.next_to))].get_random_within()
		
	def get_random_within(self):
		return [random.uniform(self.x1_walk, self.x2_walk), 0, random.uniform(self.y1_walk, self.y2_walk)]

#define the window angles
windows = [[170, 192.3], [246.4, 257.3], [281.9, 292.9],[342.2, 4.2], [76.6, 100.8]]

#define the quadrants
quadrants = [ quadrant(-max_x, -room_x, room_y, max_y), quadrant(-room_x, room_x, room_y, max_y), quadrant(room_x, max_x, room_y, max_y), quadrant(room_x, max_x, -room_y, room_y), quadrant(room_x, max_x, -max_y, -room_y), quadrant(-room_x, room_x, -max_y, -room_y), quadrant(-max_x, -room_x, -max_y, -room_y), quadrant(-max_x, -room_x, -room_y, room_y)]

quadrants[0].next_to = [quadrants[0], quadrants[1], quadrants[2], quadrants[7], quadrants[6]]
quadrants[1].next_to = [quadrants[1], quadrants[0], quadrants[2]]
quadrants[2].next_to = [quadrants[2], quadrants[1], quadrants[0], quadrants[3], quadrants[4]]
quadrants[3].next_to = [quadrants[3], quadrants[2], quadrants[4]]
quadrants[4].next_to = [quadrants[4], quadrants[3], quadrants[2], quadrants[5], quadrants[6]]
quadrants[5].next_to = [quadrants[5], quadrants[4], quadrants[6]]
quadrants[6].next_to = [quadrants[6], quadrants[5], quadrants[4], quadrants[7], quadrants[0]]
quadrants[7].next_to = [quadrants[7], quadrants[6], quadrants[0]]


for q in quadrants:
	print str(q.x1)+" "+str(q.x2)+" "+str(q.y1)+" "+str(q.y2)
	print str(q.x1_walk)+" "+str(q.x2_walk)+" "+str(q.y1_walk)+" "+str(q.y2_walk)
	print ""

def get_random_point():
	global quadrants
	return quadrants[random.randrange(0, len(quadrants))].get_random_within()

def get_quadrant( current_point ):
	#print current_point
	global quadrants
	for quad in quadrants:
		if quad.contains(current_point):
			return quad
	print "Error not in a quadrant!!!!!!!!!!!!!!"
	print current_point
	return quadrants[0]
	
	

#def get_random_point_coord( current_point ):


class a_person:
	def __init__( self ,  av_type = 0):
		self.in_quad = 0
		if av_type == 0:
			type = random.randrange(0,4)
			if type == 0:
				self.avatar = viz.add('male.cfg',viz.WORLD,scene=viz.MainScene)
			elif type == 1:
				self.avatar = viz.add('vcc_male.cfg',viz.WORLD,scene=viz.MainScene)
			elif type == 2:
				self.avatar = viz.add('female.cfg',viz.WORLD,scene=viz.MainScene)
			else:
				self.avatar = viz.add('vcc_female.cfg',viz.WORLD,scene=viz.MainScene)
		else:
			self.avatar = viz.add('vcc_male.cfg',viz.WORLD,scene=viz.MainScene)
			#Add the hat model
			self.hat = viz.add('tophat.3ds')
			self.hat.setScale([1,5,1])

			#Get the head bone of the avatar
			head = self.avatar.getBone('Bip01 Head')

			#Link the hat to the head
			HatLink = viz.link(head,self.hat)

			#Tweek the hat link so it fits snuggly on the head
			
			HatLink.preTrans( [0,0.1,-0.0] )
			HatLink.preEuler( [0,-10,0] )
			#HatLink.([0,5,0])
			
		self.avatar.setPosition(get_random_point())
		self.next_point = get_quadrant(self.avatar.getPosition()).get_random_walk()
		self.coll = 0
		self.avatar.collideMesh()
		self.avatar.enable(viz.COLLIDE_NOTIFY)
		
		#setup the AR
		viz.startlayer(viz.QUADS)
		viz.vertexcolor(1,0,0)
		#viz.pointsize(20)
		viz.linewidth(20)
		pos = self.avatar.getPosition()
		#viz.vertex(pos[0], -20, pos[2])
		#viz.vertex(pos[0], 20, pos[2])
		#rx = 0.5
		#ry = 1
		#viz.vertex(-rx, 0, 0)
		#viz.vertex(-rx, r, 0)
		#viz.vertex(r, r, 0)
		#viz.vertex(r, -r, 0)
		
		#viz.vertex(0,0,0)
		#viz.vertex(0,2,0)
		viz.vertex(-0.3,0,0)
		viz.vertex(0.3,0,0)
		viz.vertex(0.3,2,0)
		viz.vertex(-0.3,2,0)
		self.pointAR = viz.endlayer(viz.WORLD, viz.Scene2)
		self.pointAR.alpha(0.3)
		
		
		self.arev = vizact.ontimer(.01,self.move_AR)
			
			
		

	def move_AR(self):
		#why is this in the wrong position?
		apos = self.avatar.getPosition(viz.ABS_GLOBAL)
		self.pointAR.setPosition(apos, viz.ABS_GLOBAL)
		x,y,z = apos
		angle = math.atan(z/x)
		angle = angle * 180. / math.pi
		self.pointAR.setAxisAngle([0,1,0,90-angle])
		
	def custom_walk(self, points):
		self.points = points
		self.place_points = 0
		self.avatar.setPosition(points[0][0])
		self.next_point = points[0][0]
		self.next_speed = points[0][1]
		viztask.schedule(self.start_custom_walk())
		
	def stop(self):
		self.coll = 1
		
	def start_custom_walk(self):
		walk = vizact.walkTo(self.next_point, self.next_speed, 90)
		yield viztask.addAction(self.avatar, walk)
		if(self.place_points < len(self.points)):			
			self.next_point = self.points[self.place_points][0]
			self.next_speed = self.points[self.place_points][1]
			self.place_points += 1
		else:
			self.next_point = get_quadrant(self.avatar.getPosition()).get_random_walk()
			self.next_speed = random.uniform(4, 5) #change tophat speed here
		if self.coll == 0:
			##print "no collision"
			viztask.schedule(self.start_custom_walk())
	
	def walk_around( self ):
		global quadrants
		
		if random.random() > 1:#0.3:
			walk = vizact.walkTo(self.next_point)
		else:
			walk = vizact.walkTo(self.next_point, random.uniform(4, 5), 90) #change everyone else speed here
		#print self.next_point
		yield viztask.addAction(self.avatar, walk)
		self.next_point = get_quadrant(self.avatar.getPosition()).get_random_walk()
		if self.coll == 0:
			##print "no collision"
			viztask.schedule(self.walk_around())
			
	def collision( self ):
		#self.next_point = [self.next_point[0] - .1, 0, self.next_point[2] - .1] #get_quadrant(self.avatar.getPosition()).get_random_walk()#[self.avatar.getPosition()[0], 0, self.avatar.getPosition()[2] - 0.05]
		yield viztask.addAction(self.avatar, vizact.waittime(0.5))
		#self.avatar.lookat(self.next_point)
		#yield viztask.addAction(self.avatar, vizact.waittime(1))
		self.coll = 0
		viztask.schedule(self.walk_around())
		
		

def onCollideBegin(e):
	global people
	
	for person in people:
		if person.avatar == e.obj1:
			person.coll = 1
			person.avatar.clearActions()
			viztask.schedule(person.collision())
			##print "Collision detection"


viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)


	
	

def getWindow(angle):
	i = 0
	for window in windows:
		if ( (window[0]<window[1] and angle >= window[0] and angle <= window[1]) or ( window[1]<window[0] and (angle <= window[1] or angle>=window[0]))):
			return i
		i += 1
	else:
		return -1


def reportTargetAngle():
	global tophat,tophatwindow,node,tbox,tbox2,windows,tophatclicked
	global results_tbox,nfalsepos,nfalseneg,ncorrect
	[x,y,z] = tophat.avatar.getPosition()
	#print z/x
	angle = math.atan(z/x)
	angle = angle * 180. / math.pi
	if ( x < 0 ): angle += 180.
	angle += 90
	#print "angle:%f"%angle
	[y,p,r] = node.getEuler()
	y = y + 180
	angle = 360-angle
	
	msg = getWindow(angle)
	
	if ( tophatwindow == -1 and msg != -1 ):
		tophatclicked = 0
	elif ( tophatwindow != -1 and msg == -1 and tophatclicked == 0 ):
		nfalseneg += 1
		print [ncorrect, nfalsepos, nfalseneg]
	
	tophatwindow=msg
	#if(msg != -1):
	#	tbox.message("tophat window"+str(msg))
	#else:
	#	tbox.message("tophat not in a window! :(")
	#tbox2.message("tophat angle: "+str(angle))
	#print "viewing angle: ",y
	
	tbox2.message( str(ncorrect)+" "+str(nfalsepos)+" "+str(nfalseneg))

	
tbox = viz.addTextbox()	
tbox.setPosition(0.5,0.35)
tbox2 = viz.addTextbox()
tbox2.setPosition(0.5,0.65)
tbox2.visible(viz.OFF)
numtasks = 18
random_seeds = []
results = []


fov_values = [10, 20, 34]
latency_values = [1, 6, 12]



conditions = []

for i in xrange(2):
	for j in xrange(3):
		for k in xrange(3):
			conditions.append([fov_values[j], latency_values[k]])
			
random.shuffle(conditions)

for i in range(1,numtasks + 1):
	random_seeds.append(i * 3)

random.shuffle(random_seeds)

def run_tasks():
	global tbox, message, tophat, people, numtasks, random_seeds, nfalsepos, nfalseneg, ncorrect, tophatwindow, tophatclicked
	global ringbuffer_idx, ringbuffer_len
	tbox.message("Press space to start")
	for i in range(0,numtasks):
		
		yield viztask.waitKeyDown(' ')
		tbox.visible(viz.OFF)
		random.seed(random_seeds[i])
		
		nfalsepos = 0
		nfalseneg = 0
		ncorrect = 0
		tophatwindow = 0
		tophatclicked = 1
		
		setARfov( conditions[i][0] )
		ringbuffer_len = conditions[i][1]
		ringbuffer_idx = 0
		
		for j in range(0, num_av):
			people.append( a_person())
			
		tophat = a_person(1)
		people.append(tophat)
		tophat.custom_walk([[[0.1, 0, 10], 2]])#, [[-10, 0, 10], 3], [[-10, 0, -10], 4], [[10, 0, -10], 5], [[10, 0, 10], 6]])
		
		for person in people:
			viztask.schedule(person.walk_around())
			
			
		rpt = vizact.ontimer(0,reportTargetAngle)
		
		yield viztask.waitTime(45)
		results.append([ncorrect, nfalsepos, nfalseneg])
		
		vizact.removeEvent(rpt)
		vizact.removeEvent(tophat.arev)
		tophat.pointAR.remove()
		tophat.avatar.clearActions()
		tophat.avatar.remove()
		tophat.hat.remove()
		tophat.stop()
		for person in people:
			person.pointAR.remove()
			vizact.removeEvent(person.arev)
			person.avatar.clearActions()
			person.avatar.remove()
			person.stop()
			
		people = []
		tbox.visible(viz.ON)
		tbox.message("Task %d Over"%(i+1))
		print "Result: fov, latency, ncorrect, nfalsepos, nfalseneg"
		print conditions[i] +results[i]

	tbox.message("Done!")
	print "Results:"
	print "fov, latency, ncorrect, nfalsepos, nfalseneg"
	i = 0
	for r in results:
		print conditions[i] + r
		i += 1


def onKeyDown(key):
	global nfalsepos, nfalseneg, ncorrect
	if key == '4':
		ncorrect += 1
	elif key == '1':
		ncorrect -= 1
		
	elif key == '5':
		nfalsepos += 1
	elif key == '2':
		nfalsepos -= 1
		
	elif key == '6':
		nfalseneg += 1
	elif key == '3':
		nfalseneg -= 1
	
	print [ncorrect, nfalsepos, nfalseneg]

viz.callback(viz.KEYDOWN_EVENT,onKeyDown) 

people = []


viztask.schedule(run_tasks())


