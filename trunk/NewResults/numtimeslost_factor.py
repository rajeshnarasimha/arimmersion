import sys

done = False

thresh = 12
secondsLoss = 3

if len(sys.argv) == 2:
    thresh = int(sys.argv[1])

if len(sys.argv) == 3:
    thresh = int(sys.argv[1])
    secondsLoss = float(sys.argv[2])

id_dict = {}
for i in xrange(27):
    id_dict[ "%d"%i ] = "id%d"%i
fov_dict = { '10':'10deg', '20':'20deg', '34':'34deg' }
len_dict = { '0':'0.0s', '0.5':'0.5s', '1':'1.0s', '2':'2.0s' }

#resamples = open("resampled.csv")

while not done:
    for i in xrange(27):
		
		#line = resamples.readline()
		line = sys.stdin.readline()
		if line == "":
			done = True
			break
		list = line.rstrip().split(',')
		id = id_dict[list[0].lstrip()]
		fov = fov_dict[list[1].lstrip()]
		deadlen = len_dict[list[2].lstrip()]
		#fov = list[1].lstrip()
		#deadlen = list[2].lstrip()
		samples = list[3:]

		samples_in = []
		for j in samples:
			try:
				samples_in.append( float(j) )
			except:
				continue

		#print "%d samples"%len(samples_in)

		if fov != 'lowfov':
		    continue

		sys.stdout.write("%s,%s,%s,"%(id,fov,deadlen))
		totaltime = 0
		
		numLoss = 0
		reachedThreshold = 0
		timeslost = 0
		
		for j in xrange(60*60):
			if samples_in[j] > thresh:
				numLoss += 1
				
				if numLoss >= (secondsLoss*60):
					if reachedThreshold == 0:
						timeslost += 1
						reachedThreshold = 1
			else:
				numLoss = 0
				reachedThreshold = 0
		sys.stdout.write(" %d\n"%timeslost)
		
		
		
		
		
		
		
		
		
		
		
