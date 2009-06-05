import sys

f = open(sys.argv[1],'r')

line = f.readline()
participantNumber = int(line)

for i in xrange(27):
    line = f.readline()
    fov = int(line)

    line = f.readline()
    deadLength = int(line)

    line = f.readline()
    results = line

    line = f.readline()

    sys.stdout.write( "%d, %d, %d, %s"%(participantNumber,fov,deadLength,results) )

f.close()

