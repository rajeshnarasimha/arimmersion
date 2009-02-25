import viz

viz.go()
#viz.add( 'tut_ground.wrl' )
room = viz.add('../models/room/crappy_smallroom1.wrl')
room.setPosition( [0,-2,0] )
room.setEuler( [0, 90, 0] );
room.setScale( .05, .05, .05 )