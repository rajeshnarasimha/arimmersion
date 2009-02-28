import viz

TRANSLATE_INC = .2
ROTATION_INC = 4
SCALE = [0.03, 0.03, 0.03]


viz.go()
room = viz.add("justroom.obj")
room.ambient([1,1,1])
room.setScale(SCALE)
viz.MainView.setPosition(0,1.7,0)
viz.clearcolor(viz.SKYBLUE)

Karen = viz.add('vcc_female.cfg')

vizact.whilekeydown(viz.KEY_UP,viz.move,0,0,TRANSLATE_INC) #Move forward while up key is pressed
vizact.whilekeydown(viz.KEY_DOWN,viz.move,0,0,-TRANSLATE_INC) #Move backward while down key is pressed
vizact.whilekeydown(viz.KEY_LEFT,viz.rotate,viz.BODY_ORI,-ROTATION_INC,0,0) #Turn left while left arrow pressed
vizact.whilekeydown(viz.KEY_RIGHT,viz.rotate,viz.BODY_ORI,ROTATION_INC,0,0) #Turn right while right arrow pressed