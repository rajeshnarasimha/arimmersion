#datafilename="numtimes_extra8_4.csv"
datafilename="numtimeslost8_4_34.csv"
data.all=read.csv(datafilename,header=FALSE)	# read the data into a table

attach(data.all)
data.agg = aggregate(V4,list(V1,V2,V3), function(x)mean(x))
colnames(data.agg) <- c("id","fov","deadlen",'numtimes')
detach(data.all)

#aov.deadlen = aov(numtimes~deadlen+Error(id/deadlen),data.agg)
#aov.fov = aov(numtimes~deadlen+Error(id/fov),data.agg)
#aov.two = aov(numtimes~deadlen*fov+Error(id/(deadlen*fov)),data.agg)

#plot(numtimes~deadlen,data.agg,xlab='Dropout Length',ylab='Number of Times Lost')
#plot(numtimes~fov,data.agg,xlab='Field of View',ylab='Number of Times Lost')

par(mar=c(5,5,5,2),cex.axis=2,cex.lab=2)


#attach(data.agg)
#interaction.plot(fov,deadlen,numtimes,xlab='Field of View',ylab='Number of Times Lost',trace.label='Dropout Len')
#detach(data.agg)

plot(numtimes~deadlen,data.agg,cex.axis=2,cex.lab=2,xlab='Dropout Length',ylab='Number of Times Lost')
#plot(numtimes~fov,data.agg,cex.axis=2,cex.lab=2,xlab='Field of View',ylab='Number of Times Lost')
