import viz
import random
import viztask
import math

viz.go()
viz.phys.enable()
#viz.disable( viz.LIGHTING )
#light1 = viz.addLight()
#light1.position(0,5,0)
#light1.color(viz.WHITE)

env = viz.add(viz.ENVIRONMENT_MAP, 'eucalyptus\eucalyptus.jpg',scene=viz.MainScene)
sky = viz.add('skydome.dlc')
sky.texture(env)

TRANSLATE_INC = .2
ROTATION_INC = .1
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

viz.fov( HMDfov_vert, HMDaspect )
viz.window.setSize( HMDwidth, HMDheight )

ground = viz.add('tut_ground.wrl')

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




def UpdateMovement():
	global node
	node.setMatrix( viz.MainView.getMatrix() )
#	y,p,r = viz.MainView.getEuler()
#	node.setEuler([y,p,r])
#	x,y,z = viz.MainView.getPosition()
#	node.setPosition([x,y,z])
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
		viz.startlayer(viz.LINE_STRIP)
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
		viz.vertex(0,1,0)
		viz.vertex(0,1.5,0)
		self.pointAR = viz.endlayer(viz.WORLD, viz.Scene2)
		
		vizact.ontimer(.01,self.move_AR)
			
			
		

	def move_AR(self):
		#why is this in the wrong position?
		apos = self.avatar.getPosition(viz.ABS_GLOBAL)
		self.pointAR.setPosition(apos, viz.ABS_GLOBAL)
		
	def custom_walk(self, points):
		self.points = points
		self.place_points = 0
		self.avatar.setPosition(points[0])
		self.next_point = points[0]
		viztask.schedule(self.start_custom_walk())
		
	def start_custom_walk(self):
		walk = vizact.walkTo(self.next_point)
		yield viztask.addAction(self.avatar, walk)
		if(self.place_points < len(self.points)):
			self.place_points += 1
			self.next_point = self.points[self.place_points]
			if self.coll == 0:
				print "no collision"
				viztask.schedule(self.start_custom_walk())
	
	def walk_around( self ):
		global quadrants
		
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


#viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)

people = []

for i in range(0, num_av):
	people.append( a_person())
	
tophat = a_person(1)
#people.append(tophat)
tophat.custom_walk([[10, 0, 10], [-10, 0, 10], [-10, 0, -10], [10, 0, -10], [10, 0, 10]])
for person in people:
	viztask.schedule(person.walk_around())
	
	



def reportTargetAngle():
	global tophat, node,tbox,tbox2
	[x,y,z] = tophat.avatar.getPosition()
	#print z/x
	angle = math.atan(z/x)
	angle = angle * 180. / math.pi
	if ( x < 0 ): angle += 180.
	angle += 90
	#print "angle:%f"%angle
	[y,p,r] = node.getEuler()
	y = y + 180
	tbox.message("viewing angle: "+str(y))
	tbox2.message("tophat angle: "+str(360-angle))
	#print "viewing angle: ",y
	
	
tbox = viz.addTextbox()	
tbox.setPosition(0.5,0.35)
tbox2 = viz.addTextbox()
tbox2.setPosition(0.5,0.25)
vizact.ontimer(0,reportTargetAngle)

