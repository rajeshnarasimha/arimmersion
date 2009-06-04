import viz
import random
import viztask
import math
import pickle
import latinSquare
import environment_setup
import time

# text box for showing messages
tbox = viz.addTextbox()	
tbox.setPosition(0.5,0.35)

# set numtrials number to twenty-seven
numtrials = 27

# results
results = []

# load conditions from pickle
unpicklefile = open('conditions', 'r')
conditions = pickle.load(unpicklefile)
unpicklefile.close()

#for c in conditions:
#	print c.fov
#sys.exit()

participantNumber = 3 #change for each participant

# I can't believe I just wrote this
# open("results_%d.txt"%participantNumber,'w').close()

resultsPath = "results_%d_%d.txt"%(participantNumber,time.time())

# function to run the experiment
def run_tasks():
	global tbox, message, numtrials, conditions, results, participantNumber, resultsPath

	ls = latinSquare.LatinSquare(numtrials)
	order = ls.getOrder(participantNumber)
	#order[0]=0# temporary debug
	#print "order:",order
	#for i in xrange(numtrials):
	#	print ls.getOrder(i)
	#sys.exit()
	
	#for i in xrange(numtrials):
	#	print conditions[order[i]].fov
	#	print conditions[order[i]].myDeadLength
	#sys.exit()
	
	# load path set from file
	unpicklefile = open('pathGen67130', 'r')
	pg = pickle.load(unpicklefile)
	unpicklefile.close()

	# show space bar message
	tbox.message("Press space to start")

	resultsfile = open(resultsPath,'a')
	resultsfile.write("participant number: %d\n"%participantNumber)
	resultsfile.close()

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
		
		# open results file
		resultsfile = open(resultsPath,'a')

		# this is amazing and secret
		resultsfile.write("%d\n"%conditions[order[i]].fov)
		resultsfile.write("%d\n"%conditions[order[i]].myDeadLength)
		resultsfile.write(str(pg.errlist))
		resultsfile.write('\n\n')
	
		# close results file
		# using close command
		# resultsfile.close() <-- like this
		resultsfile.close()

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
