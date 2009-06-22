datafilename="timetracking_10_factor.csv"
data.all=read.csv(datafilename,header=FALSE)	# read the data into a table

#data.all[0,1] = 
#data.all[0,2] = 'fov'
#data.all[0,3] = 'deadlen'
#data.all[,'mean'] = rowMeans(data.all[,4:3603])

#plot(data.all[,'avg'],type='lines')

attach(data.all)
data.agg = aggregate(V4,list(V1,V2,V3), function(x)mean(x))
colnames(data.agg) <- c("id","fov","deadlen","tt")

#data.agg[sapply(data.agg['fov'],function(x) x==10),'fov'] = 'lowfov'
#data.agg[sapply(data.agg['fov'],function(x) x==20),'fov'] = 'medfov'
#data.agg[sapply(data.agg['fov'],function(x) x==34),'fov'] = 'uppfov'
#
#data.agg[sapply(data.agg['deadlen'],function(x) x==0),'deadlen'] = 'lowlen'
#data.agg[sapply(data.agg['deadlen'],function(x) x==1),'deadlen'] = 'medlen'
#data.agg[sapply(data.agg['deadlen'],function(x) x==2),'deadlen'] = 'upplen'
#
#data.agg[sapply(data.agg['id'],function(x) x==0),'id'] = 'id0'
#data.agg[sapply(data.agg['id'],function(x) x==1),'id'] = 'id1'
#data.agg[sapply(data.agg['id'],function(x) x==2),'id'] = 'id2'
#data.agg[sapply(data.agg['id'],function(x) x==3),'id'] = 'id3'
#data.agg[sapply(data.agg['id'],function(x) x==4),'id'] = 'id4'
#data.agg[sapply(data.agg['id'],function(x) x==5),'id'] = 'id5'
#data.agg[sapply(data.agg['id'],function(x) x==6),'id'] = 'id6'
#data.agg[sapply(data.agg['id'],function(x) x==7),'id'] = 'id7'
#data.agg[sapply(data.agg['id'],function(x) x==8),'id'] = 'id8'
#data.agg[sapply(data.agg['id'],function(x) x==9),'id'] = 'id9'

detach(data.all)

#data.sorted = data.agg[order(id,deadlen),]




aov.deadlen = aov( tt ~ deadlen + Error(id/deadlen), data.agg )
#hsd.deadlen = TukeyHSD( aov.deadlen )

#aov.fov =     aov( tt ~ fov + Error(id/fov), data.agg )
#aov.two =     aov( tt ~ (fov*deadlen) + Error(id/(fov*deadlen)), data.agg )
#
#aov2.deadlen = aov( terms( tt ~ deadlen + id, keep.order=T), data.agg )
#aov2.fov =     aov( terms( tt ~ fov + id, keep.order=T), data.agg )
#aov2.two =     aov( terms( tt ~ fov*deadlen + id, keep.order=T), data.agg )
#
#hsd.fov = TukeyHSD( aov.fov )
#hsd.two = TukeyHSD( aov.two )
#
