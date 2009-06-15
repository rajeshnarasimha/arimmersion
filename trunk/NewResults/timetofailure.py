import sys

done = False
thresh = 70
if len(sys.argv) == 2:
    thresh = int(sys.argv[1])

while not done:
    for i in xrange(27):
	line = sys.stdin.readline()
	if line == "":
	    done = True
	    break
	list = line.rstrip().split(',')
	id = list[0]
	fov = list[1]
	deadlen = list[2]
	samples = list[3:]

	samples_in = []
	for j in samples:
	    try:
		samples_in.append( float(j) )
	    except:
		continue

	#print "%d samples"%len(samples_in)

	sys.stdout.write("%s,%s,%s,"%(id,fov,deadlen))
	ttf = 3600
	for j in xrange(60*60):
	    if samples_in[j] > thresh:
		ttf = j
		break
	sys.stdout.write(" %d\n"%ttf)
