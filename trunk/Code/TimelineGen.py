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

	def addTime(self):
		self.length += 1

	def getLength(self):
		return self.length

	def setLength(self, newLength):
		self.length = newLength
	
	def isDead(self):
		return self.isDead

	def __str__(self):
		return "Event: isDead: " + str(self.isDead) + ", length: " + str(self.length)

class Timeline:
	#global settings
	trialTime = 45	#total time of a trial in seconds
	numDead = 4		#total number of dropouts
	deadLength = 2	#time of each dropout
	minLiveLength = 4	#mininum time of each live (or non-dropout) chunk of time
	totalEvents = (numDead * 2) + 1	#total number of events in trial (both dropouts and non-dropouts)
	minTotalTime = (numDead * deadLength) + (minLiveLength * numDead)
	if trialTime < minTotalTime:
			print "Bad settings, not enough trial time, need at least: " + str(minTotalTime) + " seconds"
	
	def __init__(self):
		self.onlyLiveTime = []
		self.timeline = []
		self.timeLeft = Timeline.trialTime
		
		for i in range(Timeline.totalEvents):
			if(i % 2 == 0):
				if(i == Timeline.totalEvents-1):	#create an empty live event at the end of the list
					liveEvent = Event(False, 0)
					self.timeline.append(liveEvent)
					self.onlyLiveTime.append(liveEvent)
				else:
					self.timeLeft -= Timeline.minLiveLength
					liveEvent = Event(False, Timeline.minLiveLength) #create live event
					self.timeline.append(liveEvent)
					self.onlyLiveTime.append(liveEvent)
			else:
				self.timeLeft -= Timeline.deadLength
				self.timeline.append(Event(True, Timeline.deadLength)) #create dropout event
		self.timeline[Timeline.totalEvents-1].setLength(0)

		#randomize length of live events
		for x in range(self.timeLeft):
			index = random.randrange(0, len(self.onlyLiveTime))
			self.onlyLiveTime[index].addTime()

	def getAllEvents(self):
		return self.timeline

	def getOnlyLiveEvents(self):
		return self.onlyLiveTime

	def getTimeLeft(self):
		return self.timeLeft		

def printLiveEvents(timeline):
	liveEvents = timeline.getOnlyLiveEvents()
	for i in range(len(liveEvents)):
		print liveEvents[i]

def printAllEvents(timeline):
	allEvents = timeline.getAllEvents()
	for i in range(len(allEvents)):
		print allEvents[i]

timeline = Timeline()

filename = "pickleTimeline" + str(int(time.time()) - 1240892802)
fw = open(filename, "w")
pickle.dump(timeline, fw)
fw.close()

fr = open(filename, "r")
openedTimeline = pickle.load(fr)
printAllEvents(openedTimeline)