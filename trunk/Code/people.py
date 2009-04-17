import viz
import viztask
import quadrants
import path
import random
import math
import vizact
import time

#viz.go()

quadSet = quadrants.QuadrantSet()

min_speed = 4
max_speed = 5

class a_person:
	
	def __init__( self , speedMultiplier = 1.0, av_type = 0):
		print "Creating a person"
		self.speedMultiplier = speedMultiplier
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
		self.next_point = quadSet.get_quadrant(self.avatar.getPosition())[0].get_random_walk()
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
		
		self.tracking_error = []
		#self.arev = vizact.ontimer(.01,self.move_AR)
		
		self.myquadrants = [False,False,False,False,False,False,False,False]
		self.lastTime = 0
		self.timeNotVisible = 0
		
	def move_AR(self):
		apos = self.avatar.getPosition(viz.ABS_GLOBAL)
		self.pointAR.setPosition(apos, viz.ABS_GLOBAL)
		x,y,z = apos
		angle = math.atan(z/x)
		angle = angle * 180. / math.pi
		self.pointAR.setAxisAngle([0,1,0,90-angle])
		
	def check_quadrants(self):
		theq,index = quadSet.get_quadrant(self.next_point)
		if theq != -1:
			if self.myquadrants[index] == False:
				self.save_path.quadrantsReached += 1
			self.myquadrants[index] = True
		return [theq,index]
		
	def custom_walk(self, points):
		self.points = points
		self.place_points = 0
		self.avatar.setPosition(points[0][0])
		self.check_quadrants()
		self.save_path.setStart(points[0][0])
		self.next_point = points[0][0]
		self.next_speed = points[0][1]
		self.save_path.points = []
		self.save_path.addPoint(self.next_point, self.next_speed)
		viztask.schedule(self.start_custom_walk())
		
	def stop(self):
		self.coll = 1
		
	def start_custom_walk(self):
		#self.avatar.lookat(self.next_point)
		walk = vizact.walkTo(self.next_point, self.next_speed*self.speedMultiplier, 270*self.speedMultiplier)
		yield viztask.addAction(self.avatar, walk)
		theq,index = self.check_quadrants()
		if(self.place_points < len(self.points)):		
			self.next_point = self.points[self.place_points][0]
			self.next_speed = self.points[self.place_points][1]
			self.save_path.addPoint(self.next_point, self.next_speed)
			self.place_points += 1
		elif theq != -1:
			self.myquadrants[index] = True
			self.next_point = theq.get_random_walk()
			self.next_speed = get_next_speed() #change tophat speed here
			self.save_path.addPoint(self.next_point, self.next_speed)
		if self.coll == 0:
			viztask.schedule(self.start_custom_walk())
	
	def walk_around( self ):
		global quadrants
		#self.avatar.lookat(self.next_point)
		##if random.random() > 1:
			##walk = vizact.walkTo(self.next_point)
		##else:
		walk = vizact.walkTo(self.next_point, self.next_speed*self.speedMultiplier, 270*self.speedMultiplier) #change everyone else speed here
		
		# this makes the person walk to the next point
		yield viztask.addAction(self.avatar, walk)
		
		[theq,index] = self.check_quadrants()
		if theq != -1:
			self.next_point = theq.get_random_walk()
			self.next_speed = get_next_speed()
			self.save_path.addPoint(self.next_point, self.next_speed)
			
		# self.coll == 0 always for now
		if self.coll == 0:
			viztask.schedule(self.walk_around())
		# if self.coll = 1, let collision() handle it
			
	def collision( self ):
		#do nothing for collisions
		
		#yield viztask.addAction(self.avatar, vizact.waittime(0.5))
		#self.coll = 0
		#viztask.schedule(self.walk_around())
		self.save_path.collisions += 1
		a = 0
		
	def get_path(self):
		return self.save_path
	
	def getEuler(self):
		[x,y,z] = self.avatar.getPosition()
		#print z/x
		yaw = math.atan(z/x)
		yaw *= 180. / math.pi
		if ( x < 0 ): yaw += 180.
		yaw += 90
		yaw = 360-yaw
		
		# ???
		pitch = 0
		
		roll = 0
		
		return [yaw,pitch,roll]
		
	def getWindow(self):
		[angle,foo,bar] = self.getEuler()
		i = 0
		windows = [[170, 192.3], [246.4, 257.3], [281.9, 292.9],[342.2, 4.2], [76.6, 100.8]]
		for window in windows:
			if ( (window[0]<window[1] and angle >= window[0] and angle <= window[1]) or ( window[1]<window[0] and (angle <= window[1] or angle>=window[0]))):
				return i
			i += 1
		else:
			return -1
	
	def checkVisibleTime(self):
		if self.lastTime == 0:
			self.lastTime = time.time()
			return
		now = time.time()
		if self.getWindow() == -1:			
			self.timeNotVisible += now - self.lastTime
		self.lastTime = now
		
def get_next_speed():
	global min_speed, max_speed
	return random.uniform(min_speed, max_speed)