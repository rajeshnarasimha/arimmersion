import pickle
import random
from TimelineGen import Timeline

conditions = []
FOVs = ( 10, 20, 34 )
deadLengths = ( 1, 2, 3 )

for fov in FOVs:
	for deadLength in deadLengths:
		Timeline.deadLength = deadLength
		for i in xrange(3):
			timeline = Timeline()
			timeline.fov = fov
			timeline.myDeadLength = deadLength
			conditions.append(timeline)

random.shuffle(conditions)

file = open("Conditions", 'w')
pickle.dump(conditions,file)
file.close()
