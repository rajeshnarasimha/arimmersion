import viz
import quadrants
import people
import viztask

quadSet = quadrants.QuadrantSet()

class Path:
	startPoint = []
	points = []
	
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
	speedRange = [2,5]
	collisionRange = [10,15]
	timeNotVisilbleRange = [20,30]
	pointsWalkedToRange = [5, 10]
	numberPeopleNearbyRange = [10,20]
	quadrantsReachedRange = [1,8]
	
	taskTime = 200
	numPaths = 5
	num_av = 20
	
	
	def __init__(self):
		print "AA"
		self.pathSets = []
		self.nextPath = 0
		
	def generatePaths(self):
		print "I am right here1"
		while len(self.pathSets) < self.numPaths:
			print "I am right here2"
			yield self.generateAndTestPathSet()
			if self.checkPathSet(self.nextPath):
				self.pathSets.append(self.nextPath)
		#return self.pathSets
			
			
	def checkPathSet(self, pathSet):
		if not(pathSet.speed >= self.speedRange[0] and pathSet.speed <= self.speedRange[1]):
			return False
		if not(pathSet.collisions >= self.collisionRange[0] and pathSet.collisions <= self.collisionRange[1]):
			return False
		if not(pathSet.timeNotVisible >= self.timeNotVisilbleRange[0] and pathSet.timeNotVisible <= self.timeNotVisilbleRange[1]):
			return False
		if not(pathSet.pointsWalkedTo >= self.pointsWalkedToRange[0] and pathSet.pointsWalkedTo <= self.pointsWalkedToRange[1]):
			return False
		if not(pathSet.numberPeopleNearby >= self.numberPeopleNearbyRange[0] and pathSet.numberPeopleNearby <= self.numberPeopleNearbyRange[1]):
			return False
		if not(pathSet.quadrantsReached >= self.quadrantsReachedRange[0] and pathSet.quadrantsReached <= self.quadrantsReachedRange[0]):
			return False
		return True
		
	def generateAndTestPathSet(self):
		print "I am in here"
		peopleset = []
		
		for j in range(0, self.num_av):
			peopleset.append( people.a_person())
			
		tophat = people.a_person(1)
		peopleset.append(tophat)
		tophat.custom_walk([[[0.1, 0, 10], 2]])#, [[-10, 0, 10], 3], [[-10, 0, -10], 4], [[10, 0, -10], 5], [[10, 0, 10], 6]])
		
		for person in peopleset:
			viztask.schedule(person.walk_around())
		
		yield viztask.waitTime(self.task_time)
		
		#save the path
		ps = PathSet()
		for person in peppleset:
			ps.peoplePaths.append(person.getPath())
		ps.abePath = tophat.getPath()
		
		#vizact.removeEvent(rpt)
		vizact.removeEvent(tophat.arev)
		tophat.pointAR.remove()
		tophat.avatar.clearActions()
		tophat.avatar.remove()
		tophat.hat.remove()
		tophat.stop()
		for person in peopleset:
			person.pointAR.remove()
			vizact.removeEvent(person.arev)
			person.avatar.clearActions()
			person.avatar.remove()
			person.stop()
			
		peopleset = []
		
		self.nextPath = ps
		