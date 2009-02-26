import viz
import vizact

HMDfov_vert = 36.
HMDwidth = 640.
HMDheight = 480.
HMDaspect = HMDwidth/HMDheight

viz.go()
#print dir(viz.setFov)
viz.fov( HMDfov_vert, HMDaspect )
viz.window.setSize( HMDwidth, HMDheight )

env = viz.add(viz.ENVIRONMENT_MAP, 'eucalyptus\eucalyptus.jpg',scene=viz.MainScene)
sky = viz.add('skydome.dlc')
sky.texture(env)















#viz.add( 'tut_ground.wrl' )

room = viz.add('../models/room/crappy_smallroom1.wrl',viz.WORLD,scene=viz.Scene2)
#room = viz.add('../models/room/crappy_smallroom1.wrl',viz.WORLD)
room.setPosition( [0,-2,0] )
room.setEuler( [0, 90, 0] );
room.setScale( .05, .05, .05 )

node = viz.addRenderNode()
node.setScene( viz.Scene2 )
node.setBuffer( viz.RENDER_FRAME_BUFFER )
node.setOrder( viz.POST_RENDER )
node.setInheritView( 0 )
node.setClearMask( 0 )

def setARfov( val ):
	global node, ARfov_vert
	ARfov_vert = val
	ARheight = HMDheight / HMDfov_vert * ARfov_vert
	ARwidth = ARheight * HMDaspect
	ARx = (HMDwidth - ARwidth)/2
	ARy = (HMDheight - ARheight)/2
	print ARwidth,ARheight,ARx,ARy
	node.setFov( ARfov_vert, HMDaspect, 0.1, 10 )
	node.setSize( ARwidth,ARheight,ARx,ARy )

setARfov( 20 )






def UpdateMovement():
	global node
	y,p,r = viz.MainView.getEuler()
	node.setEuler([y,p,r])
	x,y,z = viz.MainView.getPosition()
	node.setPosition([x,y,z])
vizact.ontimer(0,UpdateMovement)











fovslider = viz.addSlider()
fovslider.translate(0.2,0.1)
fovslider.set(ARfov_vert/HMDfov_vert)

def onButton(obj,state):
	global fovslider, HMDfov_vert
	if obj == fovslider:
		setARfov( HMDfov_vert * fovslider.get() )

viz.callback(viz.BUTTON_EVENT,onButton)