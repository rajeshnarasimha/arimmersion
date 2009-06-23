import pickle
import random
from TimelineGen import Timeline

conditions = []
FOVs = [ 20 ]
deadLengths = [ 0.5 ]

for fov in FOVs:
	for deadLength in deadLengths:
		Timeline.deadLength = deadLength
		for i in xrange(3):
			timeline = Timeline()
			timeline.fov = fov
			timeline.myDeadLength = deadLength
			conditions.append(timeline)

random.shuffle(conditions)

file = open("ExtraConditions", 'w')
pickle.dump(conditions,file)
file.close()
