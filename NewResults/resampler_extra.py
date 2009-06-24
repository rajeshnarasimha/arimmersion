import sys

class Resampler:
    def __init__(self,samples,timing,rate):
		self.timestep = 1. / rate
		self.samples = samples
		self.timing = timing
		self.samples.insert(0,samples[0])
		self.timing.insert(0,0)
		lastsample = self.samples[len(self.samples)-1]
		lasttiming = self.timing[len(self.timing)-1]
		for i in xrange(100):
			self.samples.append(lastsample)
			lasttiming += self.timestep
			self.timing.append(lasttiming)
		self.time = 0
    
    def step(self):
		for i in xrange( len(self.samples)-1 ):
			if self.time >= self.timing[i] and self.time <= self.timing[i+1]:
				t0 = self.timing[i]
				t1 = self.timing[i+1]
				s0 = self.samples[i]
				s1 = self.samples[i+1]
				alpha = ( self.time - t0 ) / ( t1 - t0 )
				break
		sample = alpha * s0 + ( 1. - alpha ) * s1
		self.time += self.timestep
		return (self.time,sample)

for i in xrange(27):
    samples_line = sys.stdin.readline()
    timing_line = sys.stdin.readline()
    list = samples_line.rstrip().split(',')
    id = int(list[0]) - 12
    fov = list[1]
    deadlen = list[2]
    samples = list[3:]
    list = timing_line.rstrip().split(',')
    timing = list[3:]

    samples_in = []
    timing_in = []
    for j in samples:
		try:
			samples_in.append( float(j) )
		except:
			continue
    for j in timing:
		try:
			timing_in.append( float(j) )
		except:
			continue

    if int(fov) == 20:

		#print "%d samples, %d timings"%(len(samples_in),len(timing_in))
		rs = Resampler( samples_in, timing_in, 60. )

		samples_out = []
		timing_out = []
		
		sys.stdout.write("%s,%s,%s,"%(str(id),fov,deadlen))
		for j in xrange(60*60):
			(time,sample) = rs.step()
			sys.stdout.write("%f"%sample)
			if j != 3599:
				sys.stdout.write(",")
			#samples_out.append(sample)
			#timing_out.append(time)
		sys.stdout.write("\n")
    








    
