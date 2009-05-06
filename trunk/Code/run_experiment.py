import viz
import random
import viztask
import math
import pickle
import environment_setup


# text box for showing messages
tbox = viz.addTextbox()	
tbox.setPosition(0.5,0.35)


# experiment values
numtrials = 18
fov_values = [10, 20, 34]
results = []






# build conditions list
# should use latin square to do this
# instead of random
conditions = []
for i in xrange(2):
	for j in xrange(3):
		for k in xrange(3):
			conditions.append([fov_values[j]])
random.shuffle(conditions)
random_seeds = []
for i in range(1,numtrials + 1):
	random_seeds.append(i * 3)
random.shuffle(random_seeds)

# function to run the experiment
def run_tasks():
	global tbox, message, numtrials, conditions, results

	# show space bar message
	tbox.message("Press space to start")

	# for each trial
	for i in range(0,numtrials):
		
		# wait for space bar
		yield viztask.waitKeyDown(' ')

		# hide message box
		tbox.visible(viz.OFF)

		# load path set from file
		# (latin square tells us which file to load?)
		unpicklefile = open('pathGen54565', 'r')
		pg = pickle.load(unpicklefile)
		unpicklefile.close()

		environment_setup.setARfov( conditions[i][0] )

		# run the path set
		#viztask.schedule(pg.runExperimentPathSet())
		# should this be a yield?
		yield pg.runExperimentPathSet()
		
		# append the results
		# results.append([ncorrect, nfalsepos, nfalseneg])
		
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


