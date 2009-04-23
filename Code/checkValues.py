import path
import viz
import random
import viztask
import math
import pickle

#viz.go()
viz.go()
viz.phys.enable()

#viz.disable( viz.LIGHTING )
light1 = viz.addLight()
light1.position(0,5,0)
light1.color(viz.WHITE)

#env = viz.add(viz.ENVIRONMENT_MAP, 'eucalyptus\eucalyptus.jpg',scene=viz.MainScene)
env = viz.add(viz.ENVIRONMENT_MAP, 'sky.jpg',scene=viz.MainScene)
sky = viz.add('skydome.dlc')
sky.texture(env)

TRANSLATE_INC = .2
ROTATION_INC = 2
SCALE = [0.03, 0.03, 0.03]
room = viz.add("../models/room2/room2.wrl")
room.setScale(SCALE)

ground = viz.add('tut_ground.wrl')
ground.setScale([5,1,5])
#viz.translate(viz.HEAD_POS,0,20,-20)
#viz.lookat(0,0,0)
viz.clearcolor(viz.SKYBLUE)


vizact.whilekeydown(viz.KEY_UP,viz.move,0,0,TRANSLATE_INC) #Move forward while up key is pressed
vizact.whilekeydown(viz.KEY_DOWN,viz.move,0,0,-TRANSLATE_INC) #Move backward while down key is pressed
vizact.whilekeydown(viz.KEY_LEFT,viz.rotate,viz.BODY_ORI,-ROTATION_INC,0,0) #Turn left while left arrow pressed
vizact.whilekeydown(viz.KEY_RIGHT,viz.rotate,viz.BODY_ORI,ROTATION_INC,0,0) #Turn right while right arrow pressed


def onCollideBegin(e):
	global pg
	if pg.abe.avatar == e.obj1:
		pg.abe.collision()
viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)


unpicklefile = open('pathGen68199', 'r')

pg = pickle.load(unpicklefile)

unpicklefile.close()

viztask.schedule(pg.validatePathSet())

