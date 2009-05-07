import viz
import random
import pickle
import time

#This script creates a timeline, which is just a list of events.  Each event
#is a chunk of time, either with registration dropout or without.  The createTimeline
#function creates timeline based on the global settings, with randomized times for
#live events.  All live events will have at least the minimum specified length of minLiveLength

class Event:
	def __init__(self, isDead = False, length = 0):
		self.isDead = isDead
		self.length = length
		self.startTime = 0

	def addTime(self):
		self.length += 1

	def getLength(self):
		return self.length

	def setLength(self, newLength):
		self.length = newLength
	
	def isDead(self):
		return self.isDead
		
	def setStartTime(self, startTime):
		self.startTime = startTime
		
	def getStartTime(self):
		return self.startTime

	def __str__(self):
		return "Event: isDead: " + str(self.isDead) + ", length: " + str(self.length) + ", start time: " + str(self.startTime)

class Timeline:
	#global settings
	trialTime = 45									#total time of a trial in seconds
	numDead = 4										#total number of dropouts
	deadLength = 2									#time of each dropout
	minLiveLength = 4								#mininum time of each live (or non-dropout) chunk of time
	totalEvents = (numDead * 2) + 1					#total number of events in trial (both dropouts and non-dropouts)
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
		for x in range(self.timeLeft):
			index = random.randrange(0, len(self.onlyLiveTime))
			self.onlyLiveTime[index].addTime()
			
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
			if(event.isDead()):
				vizact.ontimer2(event.getStartTime(), 0, regFunction, False)
			else:
				vizact.ontimer2(event.getStartTime(), 0, regFunction, True);

#create timeline
timeline = Timeline()

#pickle the timeline to disk
filename = "pickleTimeline" + str(int(time.time()) - 1241599999)
fw = open(filename, "w")
pickle.dump(timeline, fw)
fw.close()

#test opening the pickled file and printing info to screen
fr = open(filename, "r")
openedTimeline = pickle.load(fr)
openedTimeline.printAllEvents()