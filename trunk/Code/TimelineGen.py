import vizact
import random
import pickle
import time

#This script creates a timeline, which is just a list of events.  Each event
#is a chunk of time, either with registration dropout or without.  The createTimeline
#function creates timeline based on the global settings, with randomized times for
#live events.  All live events will have at least the minimum specified length of minLiveLength

class Event:
	def __init__(self, dead = False, length = 0):
		self.dead = dead
		self.length = length
		self.startTime = 0

	def addTime(self, subsecond):
		self.length += subsecond

	def getLength(self):
		return self.length

	def setLength(self, newLength):
		self.length = newLength
	
	def isDead(self):
		return self.dead
		
	def setStartTime(self, startTime):
		self.startTime = startTime
		
	def getStartTime(self):
		return self.startTime

	def __str__(self):
		return "Event: isDead: " + str(self.dead) + ", length: " + str(self.length) + ", start time: " + str(self.startTime)

class Timeline:
	#global settings
	trialTime = 60									#total time of a trial in seconds
	deadLength = .5									#time of each dropout
	totalDeadTime = 15								#cumulative time of all dropouts
	numDead = int(totalDeadTime / deadLength)		#total number of dropouts
	minLiveLength = 1								#mininum time of each live (or non-dropout) chunk of time
	totalEvents = (numDead * 2) + 1					#total number of events in trial (both dropouts and non-dropouts)
	subsecond = .1									#subsecond granularity of events (currently 1/10th of a second)
	minTotalTime = 0;
	
	def __init__(self):
		self.onlyLiveTime = []
		self.timeline = []
		self.timeLeft = Timeline.trialTime
		Timeline.minTotalTime = (Timeline.numDead * Timeline.deadLength) + (Timeline.minLiveLength * Timeline.numDead)
		if Timeline.trialTime < Timeline.minTotalTime:
			print "Bad settings, not enough trial time, need at least: " + str(Timeline.minTotalTime) + " seconds"
			sys.exit(0)
		
		for i in range(Timeline.totalEvents):
			if(i % 2 == 0):
				if(i == Timeline.totalEvents-1):						#create an empty live event at the end of the list
					liveEvent = Event(False, 0)
					self.timeline.append(liveEvent)
					self.onlyLiveTime.append(liveEvent)
				else:													#create live event
					self.timeLeft -= Timeline.minLiveLength
					liveEvent = Event(False, Timeline.minLiveLength) 
					self.timeline.append(liveEvent)
					self.onlyLiveTime.append(liveEvent)
			else:														#create dropout event
				self.timeLeft -= Timeline.deadLength
				self.timeline.append(Event(True, Timeline.deadLength)) 

		#randomize length of live events		
		random.seed(time.time())
		while self.timeLeft > 0.001:	#compare with something slightly greater than 0 because of imperfect floating point math
			print self.timeLeft
			index = random.randrange(0, len(self.onlyLiveTime))
			self.onlyLiveTime[index].addTime(Timeline.subsecond)
			self.timeLeft -= Timeline.subsecond
			
		#set start time of all events
		startTime = 0
		for event in self.timeline:
			event.setStartTime(startTime)
			startTime += event.getLength()

	def getAllEvents(self):
		return self.timeline

	def getOnlyLiveEvents(self):
		return self.onlyLiveTime

	def getTimeLeft(self):
		return self.timeLeft		

	def printLiveEvents(self):
		for event in self.onlyLiveTime:
			print event

	def printAllEvents(self):
		for event in self.timeline:
			print event
			
	def schedule(self, regFunction):
		for event in self.timeline:
			if (event.isDead()):
				vizact.ontimer2(event.getStartTime(), 0, regFunction, False)
			else:
				vizact.ontimer2(event.getStartTime(), 0, regFunction, True);
				
	def printTotalTime(self):
		total = 0.0
		for event in self.timeline:
			total += event.getLength()
		print "total time : " + str(total)

timeline = Timeline()
timeline.printAllEvents()