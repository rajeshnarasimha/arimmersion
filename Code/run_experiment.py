import viz
import random
import viztask
import math
import environment_setup


# text box for showing messages
tbox = viz.addTextbox()	
tbox.setPosition(0.5,0.35)


# experiment constants
numtasks = 18
fov_values = [10, 20, 34]

random_seeds = []
results = []





conditions = []

for i in xrange(2):
	for j in xrange(3):
		for k in xrange(3):
			conditions.append([fov_values[j], latency_values[k]])
			
random.shuffle(conditions)

for i in range(1,numtasks + 1):
	random_seeds.append(i * 3)

random.shuffle(random_seeds)

def run_tasks():
	global tbox, message, tophat, people, numtasks, random_seeds, nfalsepos, nfalseneg, ncorrect, tophatwindow, tophatclicked
	global ringbuffer_idx, ringbuffer_len
	tbox.message("Press space to start")
	for i in range(0,numtasks):
		
		yield viztask.waitKeyDown(' ')
		tbox.visible(viz.OFF)
		random.seed(random_seeds[i])
		
		nfalsepos = 0
		nfalseneg = 0
		ncorrect = 0
		tophatwindow = 0
		tophatclicked = 1
		
		setARfov( conditions[i][0] )
		ringbuffer_len = conditions[i][1]
		ringbuffer_idx = 0
		
		for j in range(0, num_av):
			people.append( a_person())
			
		tophat = a_person(1)
		people.append(tophat)
		tophat.custom_walk([[[0.1, 0, 10], 2]])#, [[-10, 0, 10], 3], [[-10, 0, -10], 4], [[10, 0, -10], 5], [[10, 0, 10], 6]])
		
		for person in people:
			viztask.schedule(person.walk_around())
			
			
		rpt = vizact.ontimer(0,reportTargetAngle)
		
		yield viztask.waitTime(45)
		results.append([ncorrect, nfalsepos, nfalseneg])
		
		vizact.removeEvent(rpt)
		vizact.removeEvent(tophat.arev)
		tophat.pointAR.remove()
		tophat.avatar.clearActions()
		tophat.avatar.remove()
		tophat.hat.remove()
		tophat.stop()
		for person in people:
			person.pointAR.remove()
			vizact.removeEvent(person.arev)
			person.avatar.clearActions()
			person.avatar.remove()
			person.stop()
			
		people = []
		tbox.visible(viz.ON)
		tbox.message("Task %d Over"%(i+1))
		print "Result: fov, latency, ncorrect, nfalsepos, nfalseneg"
		print conditions[i] +results[i]

	tbox.message("Done!")
	print "Results:"
	print "fov, latency, ncorrect, nfalsepos, nfalseneg"
	i = 0
	for r in results:
		print conditions[i] + r
		i += 1


def onKeyDown(key):
	global nfalsepos, nfalseneg, ncorrect
	if key == '4':
		ncorrect += 1
	elif key == '1':
		ncorrect -= 1
		
	elif key == '5':
		nfalsepos += 1
	elif key == '2':
		nfalsepos -= 1
		
	elif key == '6':
		nfalseneg += 1
	elif key == '3':
		nfalseneg -= 1
	
	print [ncorrect, nfalsepos, nfalseneg]

viz.callback(viz.KEYDOWN_EVENT,onKeyDown) 

people = []


viztask.schedule(run_tasks())


