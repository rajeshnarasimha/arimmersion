import viz
import pickle
import path


#viz.go()


pg = path.PathGenerator()

ps = path.PathSet()
ps.speed = 10
pg.pathSets.append(ps)

file = open('filename', 'w')

pickle.dump(pg,file)

file.close()

unpicklefile = open('filename', 'r')

picklepg = pickle.load(unpicklefile)

unpicklefile.close()

print "The loaded values is: " + str(picklepg.pathSets[0].speed)