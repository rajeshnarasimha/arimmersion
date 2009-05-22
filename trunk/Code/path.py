import viz
import quadrants
import people
import viztask
import pickle
import random
import vizact
import math
import error
import TimelineGen

quadSet = quadrants.QuadrantSet()
speedMultiplier = 5.0

class Path:
	#startPoint = []
	
	def __init__(self):
		self.points = []
	
		self.collisions = 0
		self.timeNotVisible = 0
		self.pointsWalkedTo = 0
		self.numberPeopleNearby = 0
		self.quadrantsReached = 0
	
	def getFullPath(self):
		#L = []
		#L = self.points[:]
		#L.insert(0, self.startPoint)
		return self.points
	
	#def setStart(self, point):
		#points = point
		#self.startPoint = point
	
	def addPoint(self, loc, speed):
		self.points.append([loc,speed])


class PathSet:
	
	
	def __init__(self):
		self.peoplePaths = []
		self.abePath = 0
		
		#need to set these variables during generateAndTestPathSet()
		self.speed = 0
		self.collisions = 0
		self.timeNotVisible = 0
		self.pointsWalkedTo = 0
		self.numberPeopleNearby = 0
		self.quadrantsReached = 0
		
class PathGenerator:
	global speedMultipler
	speedRange = [4,7]
	collisionRange = [0,1000]#[10,15] #doesn't matter
	timeNotVisibleRange = [0,50]#[60,90]
	pointsWalkedToRange = [0, 100]
	numberPeopleNearbyRange = [0,100]
	quadrantsReachedRange = [7,8]
	##turnarounds[0,0]	##max number of avatar turn-arounds allowed in a trial
	
	taskTime = 60/speedMultiplier
	numPaths = 50
	num_av = 20
	
	
	def __init__(self, filename = "pathGen" + str(random.randrange(1,100000))):
		print "AA"
		self.pathSets = []
		self.timelines = []
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
				self.timelines.append(self.nextTimeline)
				print "Saving,people:",len(self.nextPath.peoplePaths)
				#save the new path to a file
				file = open(self.filename, 'w')
				pickle.dump(self,file)
				file.close()
		#return self.pathSets
			
			
	def checkPathSet(self, pathSet):
		if not(pathSet.speed >= self.speedRange[0] and pathSet.speed <= self.speedRange[1]):
			print "Not in speed range"
			return False
		if not(pathSet.collisions >= self.collisionRange[0] and pathSet.collisions <= self.collisionRange[1]):
			print "Not in collision range"
			return False
		if not(pathSet.timeNotVisible >= self.timeNotVisibleRange[0] and pathSet.timeNotVisible <= self.timeNotVisibleRange[1]):
			print "Not in time visible range"
			return False
		if not(pathSet.pointsWalkedTo >= self.pointsWalkedToRange[0] and pathSet.pointsWalkedTo <= self.pointsWalkedToRange[1]):
			print "Not in points walked to range"
			return False
		if not(pathSet.numberPeopleNearby >= self.numberPeopleNearbyRange[0] and pathSet.numberPeopleNearby <= self.numberPeopleNearbyRange[1]):
			print "Not in people nearby to range"
			return False
		if not(pathSet.quadrantsReached >= self.quadrantsReachedRange[0] and pathSet.quadrantsReached <= self.quadrantsReachedRange[1]):
			print "Not in quadrants reached range"
			return False
		print "Saving this path"
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
		
	def checkError(self,tophat,errlist):
		err =  error.MeasureError(tophat)
		errlist.append(err)
		#print "current error: ",err
		#a = 0
	
	def runPathSet(self, peopleset, ps, tophat, custom, timeline=None):
		print "here5"
		viztask.schedule(tophat.start_custom_walk())
		if timeline != None: timeline.schedule(self.toggleAR)
		for person in peopleset:
			if custom:
				viztask.schedule(person.start_custom_walk())
			else:
				viztask.schedule(person.walk_around())
				ps = self.nextPath
		print "here6"
		self.num_nearby = 0
		self.num_samples = 0
		nearby_timer = vizact.ontimer(1/speedMultiplier,self.checkNearby,tophat,peopleset)
		
		visible_timer = vizact.ontimer(0.5/speedMultiplier,tophat.checkVisibleTime)
		
		errlist = []
		error_timer = vizact.ontimer(0.5/speedMultiplier,self.checkError,tophat,errlist)
		print "here7"
		yield viztask.waitTime(self.taskTime)
		print "here8"
		vizact.removeEvent(visible_timer)
		vizact.removeEvent(nearby_timer)
		vizact.removeEvent(error_timer)
		
		#save the path
		print "peopleSetLength:",len(peopleset)
		print "peopelPathsLenght:",len(ps.peoplePaths)
		for person in peopleset:
			ps.peoplePaths.append(person.get_path())
			print "peopelPathsLenght:",len(ps.peoplePaths)
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
		vizact.removeEvent(tophat.arev)
		tophat.arev = None	# this is so we can pickle it
		tophat.pointAR.remove()
		tophat.avatar.clearActions()
		tophat.avatar.remove()
		tophat.hat.remove()
		tophat.stop()
		for person in peopleset:
			vizact.removeEvent(person.arev)
			person.arev = None
			person.pointAR.remove()
			person.avatar.clearActions()
			person.avatar.remove()
			person.stop()
		
	
	def validatePathSet(self):
		global speedMultiplier
		#speedMultipler = 1
		for ps in self.pathSets:
			peopleset = []
			newPs = PathSet()
			print "num people",len(ps.peoplePaths)
			print "here1"
			for personPath in ps.peoplePaths:
				p = people.a_person(speedMultiplier)
				print "lencustompath:",len(personPath.getFullPath())
				print personPath.getFullPath()
				p.custom_walk(personPath.getFullPath())
				peopleset.append(p)
				print "here2"
			tophat = people.a_person(speedMultiplier, 1)
			self.abe = tophat
			tophat.custom_walk(ps.abePath.getFullPath())
			print "here3"
			yield self.runPathSet(peopleset, newPs, tophat, 1)
			
			print "Checking Differences"
			print "num collisions: ",ps.collisions,",",newPs.collisions
			print "quadrants reached: ",ps.quadrantsReached,",",newPs.quadrantsReached
			print "points to which Abe walked: ",ps.pointsWalkedTo,",",newPs.pointsWalkedTo
			print "avg. speed: ",ps.speed,",",newPs.speed
			print "time not visible: ",ps.timeNotVisible,",",newPs.timeNotVisible
			print "avg. num people nearby: ",ps.numberPeopleNearby,",",newPs.numberPeopleNearby
			
	def toggleAR( self, ARon ):
		if ARon:
			print "#############  lights back on"
		else:
			print "######### blackout"
		for p in self.peopleset:
			p.toggle_AR( ARon )
		
	def runExperimentPathSet(self, pathNum, myTimeline=None):
		global speedMultiplier
		#speedMultipler = 1
		#for ps in self.pathSets:
		print pathNum
		print len(self.pathSets)
		ps = self.pathSets[pathNum]
		if myTimeline != None:
			timeline = myTimeline
		else:
			timeline = self.timelines[pathNum]
		self.peopleset = []
		newPs = PathSet()
		for personPath in ps.peoplePaths:
			p = people.a_person(speedMultiplier)
			p.custom_walk(personPath.getFullPath())
			self.peopleset.append(p)
		tophat = people.a_person(speedMultiplier, 1)
		self.abe = tophat
		tophat.custom_walk(ps.abePath.getFullPath())
		self.peopleset.append(tophat)
		self.errlist = []
		error_timer = vizact.ontimer(0.5/speedMultiplier,self.checkError,tophat,self.errlist)
		yield self.runPathSet(self.peopleset, newPs, tophat, 1, timeline)
		vizact.removeEvent(error_timer)
	
	def generateAndTestPathSet(self):
		global speedMultiplier
		print "I am in here"
		peopleset = []
		#ps = PathSet()
		self.nextPath = PathSet()
		self.nextTimeline = TimelineGen.Timeline()
		
		for j in range(0, self.num_av):
			peopleset.append( people.a_person(speedMultiplier))
			
		tophat = people.a_person(speedMultiplier, 1)
		self.abe = tophat
		#peopleset.append(tophat)
		tophat.custom_walk([[[0.1, 0, 10], 2]])#, [[-10, 0, 10], 3], [[-10, 0, -10], 4], [[10, 0, -10], 5], [[10, 0, 10], 6]])
		
		yield self.runPathSet(peopleset, self.nextPath, tophat, 0 )
			
		#peopleset = []
		
		
		
#def onCollideBegin(e):
#	global people
#	
#	for person in people:
#		if person.avatar == e.obj1:
#			viztask.schedule(person.collision())
#			##print "Collision detection"
#
#
#viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)

