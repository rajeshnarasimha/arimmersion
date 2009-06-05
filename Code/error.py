
import viz
import math

def MeasureError(abe):
	yaw,pitch,roll = viz.MainView.getEuler()
	abeyaw,abepitch,aberoll = abe.getEuler()
	abeyaw -= 180
	#print "viewing yaw:",yaw,"tophat yaw:",abeyaw
	#err = math.sqrt( math.pow(abeyaw-yaw,2) ) + math.pow(abepitch-pitch,2) )
	err = math.fabs(abeyaw-yaw)
	if err > 180:
		err = 360 - err
		#err -= 180
	return err
	
#vizact.ontimer(0,MeasureError)
