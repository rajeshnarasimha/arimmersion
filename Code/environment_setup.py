import viz
import vizact

# general graphics setup
viz.mouse.setVisible(viz.OFF)
viz.window.setFullscreen(viz.ON)
viz.window.setBorder( viz.BORDER_NONE )
viz.go()
viz.phys.enable()
light1 = viz.addLight()
light1.position(0,5,0)
light1.color(viz.WHITE)
viz.clearcolor(viz.SKYBLUE)

# add environment map
env = viz.add(viz.ENVIRONMENT_MAP, 'sky.jpg',scene=viz.MainScene)
sky = viz.add('skydome.dlc')
sky.texture(env)

# add room model
SCALE = [0.03, 0.03, 0.03]
room = viz.add("../models/room2/room2.wrl")
room.setScale(SCALE)

# add ground model
ground = viz.add('tut_ground.wrl')
ground.setScale([5,1,5])

# keyboard controls -- for debugging only
TRANSLATE_INC = .2
ROTATION_INC = 2
vizact.whilekeydown(viz.KEY_UP,viz.move,0,0,TRANSLATE_INC) #Move forward while up key is pressed
vizact.whilekeydown(viz.KEY_DOWN,viz.move,0,0,-TRANSLATE_INC) #Move backward while down key is pressed
vizact.whilekeydown(viz.KEY_LEFT,viz.rotate,viz.BODY_ORI,-ROTATION_INC,0,0) #Turn left while left arrow pressed
vizact.whilekeydown(viz.KEY_RIGHT,viz.rotate,viz.BODY_ORI,ROTATION_INC,0,0) #Turn right while right arrow pressed

# HMD constants (for real world view)
HMDfov_vert = 36.
HMDwidth = 640.
HMDheight = 480.
HMDnear = 1
HMDfar = 1000
HMDaspect = HMDwidth/HMDheight

# set up real world view parameters
viz.fov( HMDfov_vert, HMDaspect )
viz.window.setSize( HMDwidth, HMDheight )

# set up AR view rendering node (Scene 2)
node = viz.addRenderNode()
node.setScene( viz.Scene2 )
node.setBuffer( viz.RENDER_FRAME_BUFFER )
node.setOrder( viz.POST_RENDER )
node.setInheritView( 0 )
node.setClearMask( 0 )
node.disable(viz.DEPTH_TEST)

# set up 2D AR overlay for gray box and crosshairs (Scene 3)
node2D = viz.addRenderNode()
node2D.setScene(viz.Scene3)
node2D.setBuffer( viz.RENDER_FRAME_BUFFER )
node2D.setOrder( viz.POST_RENDER )
node2D.setInheritView(0)
node2D.setSize( HMDwidth,HMDheight )
node2D.setProjectionMatrix(viz.Matrix.ortho2D(0,HMDwidth,0,HMDheight))
node2D.setClearMask(0)
node2D.disable(viz.DEPTH_TEST)

# add crosshairs
viz.startlayer(viz.LINES)
viz.vertexcolor([1,0,0])
viz.vertex([HMDwidth/2-10,HMDheight/2,0])
viz.vertex([HMDwidth/2+10,HMDheight/2,0])
viz.vertex([HMDwidth/2,HMDheight/2-10,0])
viz.vertex([HMDwidth/2,HMDheight/2+10,0])
viz.vertexcolor([1,1,1])
viz.endlayer(viz.WORLD,viz.Scene3)

# function to display AR view
ARgraybox = 0
def setARfov( val ):
	global HMDheight, HMDwidth, HMDfov_vert, HMDaspect, HMDnear, HMDfar
	global node, ARfov_vert, ARgraybox
	
	ARfov_vert = 10
	ARheight = (int) (HMDheight / HMDfov_vert * ARfov_vert)
	ARwidth = ARheight * HMDaspect
	
	ARx = (HMDwidth - ARwidth)/2
	ARy = (HMDheight - ARheight)/2
	node.setSize( ARwidth,ARheight,ARx,ARy )
	node.setFov( ARfov_vert, HMDaspect, HMDnear, HMDfar )
	
	if(ARgraybox != 0):
		ARgraybox.remove()
	viz.startlayer(viz.QUADS)
	viz.vertex([ARx,ARy,0])
	viz.vertex([ARx + ARwidth, ARy,0])
	viz.vertex([ARx + ARwidth,ARy + ARheight,0])
	viz.vertex([ARx,ARy + ARheight,0])
	ARgraybox = viz.endlayer(viz.WORLD,viz.Scene3)
	ARgraybox.alpha(0.15)

# set initial AR fov to 20
setARfov( 20 )

# set up tracker
tracker = viz.add('intersense.dls')	

# function to apply tracker data
def UpdateMovement():
	global tracker
	global node
	
	# get tracker euler rotation
	yaw,pitch,roll = tracker.getEuler()

	# set main view rotation to tracker output
	viz.MainView.setEuler([yaw,pitch,roll])

	# update AR node with current pose
	node.setPosition( viz.MainView.getPosition() )
	node.setEuler( viz.MainView.getEuler() )
	
# add tracker update timer 
vizact.ontimer(0,UpdateMovement)









