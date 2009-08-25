#datafilename="extratt8.csv"
datafilename="tt8.csv"
data.all=read.csv(datafilename,header=FALSE)	# read the data into a table

attach(data.all)
data.agg = aggregate(V4,list(V1,V2,V3), function(x)mean(x))
colnames(data.agg) <- c("id","fov","deadlen","tt")

detach(data.all)




#aov.deadlen = aov( tt ~ deadlen + Error(id/deadlen), data.agg )
#aov.fov =     aov( TimeTracking ~ FieldOfView + Error(id/FieldOfView), data.agg )
aov.two =     aov( tt ~ (fov*deadlen) + Error(id/(fov*deadlen)), data.agg )

#hsd.deadlen = TukeyHSD( aov.deadlen )

#aov2.deadlen = aov( terms( tt ~ deadlen + id, keep.order=T), data.agg )
#aov2.fov =     aov( terms( tt ~ fov + id, keep.order=T), data.agg )
#aov2.two =     aov( terms( tt ~ fov*deadlen + id, keep.order=T), data.agg )
#
#hsd.fov = TukeyHSD( aov.fov )
#hsd.two = TukeyHSD( aov.two )
#

#boxplot( tt ~ deadlen, data.agg )
#boxplot( tt ~ fov, data.agg )

#plot(tt~fov,data.agg,xlab='Field of View',ylab='Time Following Target')
#plot(tt~deadlen,data.agg,xlab='Dropout Length',ylab='Time Following Target')

#attach(data.agg)
#interaction.plot(fov,deadlen,tt)
#detach(data.agg)


par(mar=c(5,5,5,2),cex.axis=2,cex.lab=2)
plot(tt~deadlen,data.agg,xlab='Dropout Length',ylab='Time Following Target (s)')
#plot(tt~fov,data.agg,xlab='Field of View',ylab='Time Following Target (s)')
