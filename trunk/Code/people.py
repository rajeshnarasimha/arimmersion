import viz
import viztask
import quadrants
import path
import random
import math

#viz.go()

quadSet = quadrants.QuadrantSet()

min_speed = 4
max_speed = 5

class a_person:
	
	def __init__( self ,  av_type = 0):
		print "Creating a person"
		self.save_path = path.Path()
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
			
		self.avatar.setPosition(quadSet.get_random_point())
		self.save_path.setStart(self.avatar.getPosition())
		self.next_point = quadSet.get_quadrant(self.avatar.getPosition()).get_random_walk()
		self.next_speed = get_next_speed()
		self.save_path.addPoint(self.next_point, self.next_speed)
		self.coll = 0
		self.avatar.collideMesh()
		self.avatar.enable(viz.COLLIDE_NOTIFY)
		
		#setup the AR
		viz.startlayer(viz.QUADS)
		viz.vertexcolor(1,0,0)
		viz.linewidth(20)
		pos = self.avatar.getPosition()
		viz.vertex(-0.3,0,0)
		viz.vertex(0.3,0,0)
		viz.vertex(0.3,2,0)
		viz.vertex(-0.3,2,0)
		self.pointAR = viz.endlayer(viz.WORLD, viz.Scene2)
		self.pointAR.alpha(0.3)
		
		#self.arev = vizact.ontimer(.01,self.move_AR)
		

	def move_AR(self):
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
		self.save_path.setStart(points[0][0])
		self.next_point = points[0][0]
		self.next_speed = points[0][1]
		self.save_path.points = []
		self.save_path.addPoint(self.next_point, self.next_speed)
		viztask.schedule(self.start_custom_walk())
		
	def stop(self):
		self.coll = 1
		
	def start_custom_walk(self):
		walk = vizact.walkTo(self.next_point, self.next_speed, 90)
		yield viztask.addAction(self.avatar, walk)
		if(self.place_points < len(self.points)):			
			self.next_point = self.points[self.place_points][0]
			self.next_speed = self.points[self.place_points][1]
			self.save_path.addPoint(self.next_point, self.next_speed)
			self.place_points += 1
		else:
			theq = quadSet.get_quadrant(self.next_point)
			if theq != -1:
				self.next_point = theq.get_random_walk()
				self.next_speed = get_next_speed() #change tophat speed here
				self.save_path.addPoint(self.next_point, self.next_speed)
		if self.coll == 0:
			viztask.schedule(self.start_custom_walk())
	
	def walk_around( self ):
		global quadrants
		
		if random.random() > 1:
			walk = vizact.walkTo(self.next_point)
		else:
			walk = vizact.walkTo(self.next_point, self.next_speed, 90) #change everyone else speed here
		yield viztask.addAction(self.avatar, walk)
		theq = quadSet.get_quadrant(self.avatar.getPosition())
		if theq != -1:
			self.next_point = theq.get_random_walk()
			self.next_speed = get_next_speed()
			self.save_path.addPoint(self.next_point, self.next_speed)
		if self.coll == 0:
			viztask.schedule(self.walk_around())
			
	def collision( self ):
		#do nothing for collisions
		
		#yield viztask.addAction(self.avatar, vizact.waittime(0.5))
		#self.coll = 0
		#viztask.schedule(self.walk_around())
		a = 0
		
	def get_path(self):
		return self.self.save_path
		
def get_next_speed():
	global min_speed, max_speed
	return random.uniform(min_speed, max_speed)