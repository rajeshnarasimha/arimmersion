import viz
import random
import viztask
import math
import pickle
import latinSquare
import environment_setup

# text box for showing messages
tbox = viz.addTextbox()	
tbox.setPosition(0.5,0.35)


# experiment values
numtrials = 27
fov_values = [10, 20, 34]
results = []






# build conditions list
# should use latin square to do this
# instead of random
#conditions = []
#for i in xrange(3):
#	for j in xrange(3):
#		for k in xrange(3):
#			conditions.append([fov_values[j]])
#random.shuffle(conditions)
#random_seeds = []
#for i in range(1,numtrials + 1):
#	random_seeds.append(i * 3)
#random.shuffle(random_seeds)

unpicklefile = open('conditions', 'r')
conditions = pickle.load(unpicklefile)
unpicklefile.close()

#for c in conditions:
#	print c.fov
#sys.exit()

# function to run the experiment
def run_tasks():
	global tbox, message, numtrials, conditions, results

	participantNumber = 20 #change for each participant
	ls = latinSquare.LatinSquare(numtrials)
	order = ls.getOrder(participantNumber)
	#order[0]=0# temporary debug
	#print "order:",order
	#for i in xrange(numtrials):
	#	print ls.getOrder(i)
	#sys.exit()
	
	# load path set from file
	unpicklefile = open('pathGen67130', 'r')
	pg = pickle.load(unpicklefile)
	unpicklefile.close()

	# show space bar message
	tbox.message("Press space to start")

	# for each trial
	for i in range(0,numtrials):
		
		# wait for space bar
		yield viztask.waitKeyDown(' ')

		# hide message box
		tbox.visible(viz.OFF)

		# set up variables for this condition
		environment_setup.setARfov( conditions[order[i]].fov )
		
		# run the path set
		yield pg.runExperimentPathSet(order[i],conditions[order[i]])
		
		# append the results
		# results.append([ncorrect, nfalsepos, nfalseneg])
		results.append( pg.errlist )
		print pg.errlist
		
		# show trial over message
		tbox.visible(viz.ON)
		tbox.message("Trial %d Over"%(i+1))
		#print "Result: fov, latency, ncorrect, nfalsepos, nfalseneg"
		#print conditions[i] +results[i]

	# show done message
	tbox.message("Done!")

	# print results
	#print "Results:"
	#print "fov, latency, ncorrect, nfalsepos, nfalseneg"
	#i = 0
	#for r in results:
		#print conditions[i] + r
		#i += 1


# run it
viztask.schedule(run_tasks())


# call timeline() to create
# get events
# iterate through list
# get start time, isdead
