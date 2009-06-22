import sys

done = False

id_dict = {}
for i in xrange(27):
    id_dict[ "%d"%i ] = "id%d"%i
fov_dict = { '10':'lowfov', '20':'medfov', '34':'uppfov' }
len_dict = { '0':'lowlen', '1':'medlen', '2':'upplen' }

while not done:
    for i in xrange(27):
	line = sys.stdin.readline()
	if line == "":
	    done = True
	    break
	list = line.rstrip().split(',')
	id = id_dict[list[0].lstrip()]
	fov = fov_dict[list[1].lstrip()]
	deadlen = len_dict[list[2].lstrip()]
	samples = list[3:]

	samples_in = []
	for j in samples:
	    try:
		samples_in.append( float(j) )
	    except:
		continue

	#print "%d samples"%len(samples_in)

	sys.stdout.write("%s,%s,%s,"%(id,fov,deadlen))
	totaltime = 0.
	for j in xrange(3600):
	    totaltime += samples_in[j]
	sys.stdout.write("%lf\n"%(totaltime/3600.))
