import sys

done = False

thresh = 12
secondsLoss = 2

if len(sys.argv) == 2:
    thresh = int(sys.argv[1])

id_dict = {}
for i in xrange(27):
    id_dict[ "%d"%i ] = "id%d"%i
fov_dict = { '10':'lowfov', '20':'medfov', '34':'uppfov' }
len_dict = { '0':'lowlen', '1':'medlen', '2':'upplen' }

resamples = open("resampled.csv")

while not done:
    for i in xrange(27):
		
		line = resamples.readline()
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
		
		
		
		
		
		
		
		
		
		
		
