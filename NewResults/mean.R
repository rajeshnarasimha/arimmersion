datafilename="mean.csv"
data.all=read.csv(datafilename,header=FALSE)	# read the data into a table

#data.all[,'mean'] = rowMeans(data.all[,4:3603])

attach(data.all)
data.agg = aggregate(V4,list(V1,V2,V3), function(x)mean(x))
colnames(data.agg) <- c("id","fov","deadlen",'mean')
detach(data.all)

aov.two = aov(numtimes~deadlen*fov+Error(id/(deadlen*fov)),data.agg)

attach(data.agg)
interaction.plot(fov,deadlen,numtimes)
detach(data.agg)
