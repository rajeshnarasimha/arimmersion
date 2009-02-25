import viz
import vizact
#viz.go()

viz.add( 'tut_ground.wrl' )

#import viztracker
#PORT_INTERSENSE = 0
#track = viz.add('intersense.dls')
#print dir(track)
#track = viz.addOri()
#viz.link(track,viz.MainView)

import viz

viz.go()
#viz.add( 'tut_ground.wrl' )

import vizinfo
vizinfo.add('This script demonstrates how to perform manual head tracking.\nIt will retrieve data from the tracker and only rotate the yaw.\nBy default this script will connect to an intersense.\nPress the \'r\' key to reset the tracker')

#Add environment
#viz.add('gallery.ive')
viz.add('../models/crappy_smallroom1.wrl')

#Add the intersense plugin
PORT_INTERSENSE = 0
tracker = viz.add('intersense.dls')

ringbuffer_len = 20
yaw_ringbuffer = range(ringbuffer_len)
pitch_ringbuffer = range(ringbuffer_len)
roll_ringbuffer = range(ringbuffer_len)
for i in range(ringbuffer_len):
	yaw_ringbuffer[i] = 0
	pitch_ringbuffer[i] = 0
	roll_ringbuffer[i] = 0
ringbuffer_idx = 0

# This function will grab the tracker data and update the viewpoint
def UpdateView():
	global yaw_ringbuffer, pitch_ringbuffer, roll_ringbuffer, ringbuffer_idx
	
	#yaw,pitch,roll = tracker.getEuler()
	#viz.MainView.setEuler([yaw,pitch,roll],viz.BODY_ORI)
	#return
	
	yaw = yaw_ringbuffer[ringbuffer_idx]
	pitch = pitch_ringbuffer[ringbuffer_idx]
	roll = roll_ringbuffer[ringbuffer_idx]
	#Only rotate the yaw of the body orientation

	viz.MainView.setEuler([yaw,pitch,roll],viz.BODY_ORI)
	#Get tracker euler rotation
	yaw,pitch,roll = tracker.getEuler()
	yaw_ringbuffer[ringbuffer_idx] = yaw
	pitch_ringbuffer[ringbuffer_idx] = pitch
	roll_ringbuffer[ringbuffer_idx] = roll
	
	ringbuffer_idx = (ringbuffer_idx + 1)%len(yaw_ringbuffer)
	
	
#Call UpdateView function every frame
vizact.ontimer(0,UpdateView)

#Rest tracker when 'r' key is pressed
vizact.onkeydown('r',tracker.reset) 