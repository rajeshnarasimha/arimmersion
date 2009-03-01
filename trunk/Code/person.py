import viz
import random
import viztask


viz.go()
viz.phys.enable()

TRANSLATE_INC = .2
ROTATION_INC = 4
SCALE = [0.03, 0.03, 0.03]
room = viz.add("../models/room2/room2.wrl")
room.setScale(SCALE)

vizact.whilekeydown(viz.KEY_UP,viz.move,0,0,TRANSLATE_INC) #Move forward while up key is pressed
vizact.whilekeydown(viz.KEY_DOWN,viz.move,0,0,-TRANSLATE_INC) #Move backward while down key is pressed
vizact.whilekeydown(viz.KEY_LEFT,viz.rotate,viz.BODY_ORI,-ROTATION_INC,0,0) #Turn left while left arrow pressed
vizact.whilekeydown(viz.KEY_RIGHT,viz.rotate,viz.BODY_ORI,ROTATION_INC,0,0) #Turn right while right arrow pressed

HMDfov_vert = 36.
HMDwidth = 640.
HMDheight = 480.
HMDaspect = HMDwidth/HMDheight

ground = viz.add('tut_ground.wrl')

#viz.translate(viz.HEAD_POS,0,20,-20)
#viz.lookat(0,0,0)
viz.clearcolor(viz.SKYBLUE)

#window = viz.add(viz.WINDOW)
#window.setPosition(.5,.5)


node = viz.addRenderNode()
node.setScene( viz.Scene1 )
node.setBuffer( viz.RENDER_FRAME_BUFFER )
node.setOrder( viz.POST_RENDER )
node.setInheritView( 0 )
node.setClearMask( 0 )

def setARfov( val ):
	global node, ARfov_vert
	ARfov_vert = val
	ARheight = HMDheight / HMDfov_vert * ARfov_vert
	ARwidth = ARheight * HMDaspect
	ARx = (HMDwidth - ARwidth)/2
	ARy = (HMDheight - ARheight)/2
	print ARwidth,ARheight,ARx,ARy
	node.setFov( ARfov_vert, HMDaspect, 0.1, 10 )
	node.setSize( ARwidth,ARheight,ARx,ARy )

setARfov( 20 )



def UpdateMovement():
	global node
	y,p,r = viz.MainView.getEuler()
	node.setEuler([y,p,r])
	x,y,z = viz.MainView.getPosition()
	node.setPosition([x,y,z])
vizact.ontimer(0,UpdateMovement)

fovslider = viz.addSlider()
fovslider.translate(0.2,0.1)
fovslider.set(ARfov_vert/HMDfov_vert)

def onButton(obj,state):
	global fovslider, HMDfov_vert
	if obj == fovslider:
		setARfov( HMDfov_vert * fovslider.get() )

viz.callback(viz.BUTTON_EVENT,onButton)



#Create custom camera handler
#class MyCameraHandler( viz.CameraHandler ):
#
#	def _camUpdate( self, e ):
#		if viz.iskeydown( viz.KEY_RIGHT ):
#			e.view.rotate(0,1,0,1,viz.BODY_ORI,viz.REL_PARENT)
#			#e.view2.rotate(0,1,0,1,viz.BODY_ORI,viz.REL_PARENT)
#		elif viz.iskeydown ( viz.KEY_LEFT ):
#			#move view up
#			e.view.rotate(0,1,0,-1,viz.BODY_ORI,viz.REL_PARENT)
#			#e.view2.rotate(0,1,0,-1,viz.BODY_ORI,viz.REL_PARENT)
#
#viz.cam.setHandler( MyCameraHandler() )


num_av = 20
real_room_x = 5
room_x = real_room_x + 2
real_room_y = 5
room_y = real_room_y + 2
max_x = 20
max_y = 20

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




class quadrant:
	next_to = []
	
	def __init__(self, x1, x2, y1, y2):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
	
	def contains(self, point):
		print point
		print [self.x1, self.x2]
		print [self.y1, self.y2]
		if self.x1 <= point[0] and self.x2 > point[0]:
			if self.y1 <= point[2] and self.y2 > point[2]:
				return True
		return False
		
	def get_random_walk(self):
		return self.next_to[random.randrange(0, len(self.next_to))].get_random_within()
		
	def get_random_within(self):
		return [random.uniform(self.x1, self.x2), 0, random.uniform(self.y1, self.y2)]
	
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


def get_random_point():
	global quadrants
	return quadrants[random.randrange(0, len(quadrants))].get_random_within()

def get_quadrant( current_point ):
	#print current_point
	global quadrants
	for quad in quadrants:
		if quad.contains(current_point):
			return quad
	print "Error not in a quadrant!"
	return quadrants[0]
	
	

#def get_random_point_coord( current_point ):


class a_person:
	def __init__( self ,  av_type = 0):
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
			hat = viz.add('tophat.3ds')
			hat.setScale([1,5,1])

			#Get the head bone of the avatar
			head = self.avatar.getBone('Bip01 Head')

			#Link the hat to the head
			HatLink = viz.link(head,hat)

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
		viz.startlayer(viz.LINES)
		viz.vertexcolor(1,0,0)
		viz.pointsize(20)
		pos = self.avatar.getPosition()
		#viz.vertex(pos[0], -20, pos[2])
		#viz.vertex(pos[0], 20, pos[2])
		viz.vertex(0, -20, 0)
		viz.vertex(0, 20, 0)
		self.pointAR = viz.endlayer(viz.WORLD, viz.Scene1)
		
		vizact.ontimer(.01,self.move_AR)
			
			
		

	def move_AR(self):
		#why is this in the wrong position?
		apos = self.avatar.getPosition(viz.ABS_GLOBAL)
		self.pointAR.setPosition(apos, viz.ABS_GLOBAL)
	
	def walk_around( self ):
		
		if random.random() > 0.3:
			walk = vizact.walkTo(self.next_point)
		else:
			walk = vizact.walkTo(self.next_point, random.uniform(1, 3), 90)
		
		yield viztask.addAction(self.avatar, walk)
		self.next_point = get_quadrant(self.avatar.getPosition()).get_random_walk()
		if self.coll == 0:
			print "no collision"
			viztask.schedule(self.walk_around())
			
	def collision( self ):
		self.next_point = [self.next_point[0] - .1, 0, self.next_point[2] - .1] #get_quadrant(self.avatar.getPosition()).get_random_walk()#[self.avatar.getPosition()[0], 0, self.avatar.getPosition()[2] - 0.05]
		yield viztask.addAction(self.avatar, vizact.waittime(1))
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
			print "Collision detection"


viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)

people = []

for i in range(0, num_av):
	people.append( a_person())
	
tophat = a_person(1)
people.append(tophat)

for person in people:
	viztask.schedule(person.walk_around())
	