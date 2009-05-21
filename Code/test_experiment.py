import viz
import random
import viztask
import math
import pickle
import latinSquare
import environment_setup
from TimelineGen import Timeline

# file to unpickle
pickle_path = 'pathGen93238'

# experiment settings go here
test_fov = 5
Timeline.trialTime = 60
Timeline.numDead = 5
Timeline.deadLength = 1.5
Timeline.minLiveLength = 4
numtrials = 27
test_timeline = Timeline()

# text box for showing messages
tbox = viz.addTextbox()	
tbox.setPosition(0.5,0.35)

# function to run the experiment
def run_tasks():
	global pickle_path
	global tbox, message, numtrials, test_fov, test_timeline

	# load path set from file
	unpicklefile = open(pickle_path, 'r')
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
		environment_setup.setARfov( test_fov )
		
		# run the path set
		yield pg.runExperimentPathSet(i, test_timeline)
				
		# show trial over message
		tbox.visible(viz.ON)
		tbox.message("Trial %d Over"%(i+1))

	# show done message
	tbox.message("Done!")

# run it
viztask.schedule(run_tasks())

# make paths
# try them until we get a good one
# then tweak the settings