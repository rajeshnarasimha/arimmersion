import viz

viz.go()
#viz.add( 'tut_ground.wrl' )
room = viz.add('../models/room/crappy_smallroom1.wrl',viz.WORLD,1)
room.setPosition( [0,-2,0] )
room.setEuler( [0, 90, 0] );
room.setScale( .05, .05, .05 )

env = viz.add(viz.ENVIRONMENT_MAP, 'eucalyptus\eucalyptus.jpg')
sky = viz.add('skydome.dlc')
sky.texture(env)