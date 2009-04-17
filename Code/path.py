import viz
import quadrants
import people
import viztask
import pickle
import random
import vizact
import math

quadSet = quadrants.QuadrantSet()
speedMultiplier = 50.0

class Path:
	startPoint = []
	points = []
	
	collisions = 0
	timeNotVisible = 0
	pointsWalkedTo = 0
	numberPeopleNearby = 0
	quadrantsReached = 0
	
	def setStart(self, point):
		points = point
	
	def addPoint(self, loc, speed):
		self.points.append([loc,speed])


class PathSet:
	peoplePaths = []
	abePath = []
	
	#need to set these variables during generateAndTestPathSet()
	speed = 0
	collisions = 0
	timeNotVisible = 0
	pointsWalkedTo = 0
	numberPeopleNearby = 0
	quadrantsReached = 0

class PathGenerator:
	global speedMultipler
	speedRange = [2,5]
	collisionRange = [0,1000]#[10,15] #doesn't matter
	timeNotVisibleRange = [60,90]
	pointsWalkedToRange = [15, 23]
	numberPeopleNearbyRange = [2,6]
	quadrantsReachedRange = [5,8]
	##turnarounds[0,0]	##max number of avatar turn-arounds allowed in a trial
	
	taskTime = 100/speedMultiplier
	numPaths = 5
	num_av = 20
	
	
	def __init__(self, filename = "pathGen" + str(random.randrange(1,100000))):
		print "AA"
		self.pathSets = []
		#self.nextPath = 0
		self.filename = filename
		#save the new path to a file
		#file = open(self.filename, 'w')
		#pickle.dump(self,file)
		#file.close()
		#just to test working
		##unpicklefile = open(self.filename, 'r')
		##picklepg = pickle.load(unpicklefile)
		##unpicklefile.close()
		##print "The loaded values is: " + str(picklepg.taskTime)
		
	def generatePaths(self):
		print "I am right here1"
		while len(self.pathSets) < self.numPaths:
			print "I am right here2"
			yield self.generateAndTestPathSet()
			if self.checkPathSet(self.nextPath):
				self.pathSets.append(self.nextPath)
				#save the new path to a file
				file = open(self.filename, 'w')
				pickle.dump(self,file)
				file.close()
		#return self.pathSets
			
			
	def checkPathSet(self, pathSet):
		if not(pathSet.speed >= self.speedRange[0] and pathSet.speed <= self.speedRange[1]):
			return False
		if not(pathSet.collisions >= self.collisionRange[0] and pathSet.collisions <= self.collisionRange[1]):
			return False
		if not(pathSet.timeNotVisible >= self.timeNotVisibleRange[0] and pathSet.timeNotVisible <= self.timeNotVisibleRange[1]):
			return False
		if not(pathSet.pointsWalkedTo >= self.pointsWalkedToRange[0] and pathSet.pointsWalkedTo <= self.pointsWalkedToRange[1]):
			return False
		if not(pathSet.numberPeopleNearby >= self.numberPeopleNearbyRange[0] and pathSet.numberPeopleNearby <= self.numberPeopleNearbyRange[1]):
			return False
		if not(pathSet.quadrantsReached >= self.quadrantsReachedRange[0] and pathSet.quadrantsReached <= self.quadrantsReachedRange[0]):
			return False
		return True
	
	def checkNearby(self,tophat,peopleset):
		tophat_pt = tophat.avatar.getPosition()
		num_nearby = 0
		for p in peopleset:
			pt = p.avatar.getPosition()
			dist = math.pow(pt[0]-tophat_pt[0],2) + math.pow(pt[1]-tophat_pt[1],2)
			if dist < 7*7:
				num_nearby += 1
		self.num_nearby += num_nearby
		self.num_samples += 1
		
	def generateAndTestPathSet(self):
		global speedMultiplier
		print "I am in here"
		peopleset = []
		ps = PathSet()
		
		for j in range(0, self.num_av):
			peopleset.append( people.a_person(speedMultiplier))
			
		tophat = people.a_person(speedMultiplier, 1)
		self.abe = tophat
		#peopleset.append(tophat)
		tophat.custom_walk([[[0.1, 0, 10], 2]])#, [[-10, 0, 10], 3], [[-10, 0, -10], 4], [[10, 0, -10], 5], [[10, 0, 10], 6]])
		
		for person in peopleset:
			viztask.schedule(person.walk_around())
		
		self.num_nearby = 0
		self.num_samples = 0
		nearby_timer = vizact.ontimer(1/speedMultiplier,self.checkNearby,tophat,peopleset)
		
		visible_timer = vizact.ontimer(0.5/speedMultiplier,tophat.checkVisibleTime)
		
		yield viztask.waitTime(self.taskTime)
		
		vizact.removeEvent(visible_timer)
		vizact.removeEvent(nearby_timer)
		
		#save the path
		for person in peopleset:
			ps.peoplePaths.append(person.get_path())
		ps.abePath = tophat.get_path()
		
		ps.speed = 0
		for pt in ps.abePath.points:
			ps.speed += pt[1]
		ps.speed /= len(ps.abePath.points)
		ps.collisions = ps.abePath.collisions
		ps.timeNotVisible = tophat.timeNotVisible*speedMultiplier
		ps.pointsWalkedTo = len( ps.abePath.points )
		ps.numberPeopleNearby = self.num_nearby / self.num_samples
		ps.quadrantsReached = ps.abePath.quadrantsReached
		print "num collisions: ",ps.collisions
		print "quadrants reached: ",ps.quadrantsReached
		print "points to which Abe walked: ",ps.pointsWalkedTo
		print "avg. speed: ",ps.speed
		print "time not visible: ",ps.timeNotVisible
		print "avg. num people nearby: ",ps.numberPeopleNearby
		#vizact.removeEvent(rpt)
		#vizact.removeEvent(tophat.arev)
		tophat.pointAR.remove()
		tophat.avatar.clearActions()
		tophat.avatar.remove()
		tophat.hat.remove()
		tophat.stop()
		for person in peopleset:
			person.pointAR.remove()
			#vizact.removeEvent(person.arev)
			person.avatar.clearActions()
			person.avatar.remove()
			person.stop()
			
		peopleset = []
		
		self.nextPath = ps
		
def onCollideBegin(e):
	global people
	
	for person in people:
		if person.avatar == e.obj1:
			viztask.schedule(person.collision())
			##print "Collision detection"


viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)

