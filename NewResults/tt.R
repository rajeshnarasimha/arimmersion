datafilename="timetracking_20.csv"
data.all=read.csv(datafilename,header=FALSE)	# read the data into a table

#data.all[0,1] = 
#data.all[0,2] = 'fov'
#data.all[0,3] = 'deadlen'
#data.all[,'mean'] = rowMeans(data.all[,4:3603])

#plot(data.all[,'avg'],type='lines')

attach(data.all)
data.agg = aggregate(V4,list(V1,V2,V3), function(x)mean(x))
colnames(data.agg) <- c("id","fov","deadlen","tt")

data.agg[sapply(data.agg['fov'],function(x) x==10),'fov'] = 'lowfov'
data.agg[sapply(data.agg['fov'],function(x) x==20),'fov'] = 'medfov'
data.agg[sapply(data.agg['fov'],function(x) x==34),'fov'] = 'uppfov'

data.agg[sapply(data.agg['deadlen'],function(x) x==0),'deadlen'] = 'lowlen'
data.agg[sapply(data.agg['deadlen'],function(x) x==1),'deadlen'] = 'medlen'
data.agg[sapply(data.agg['deadlen'],function(x) x==2),'deadlen'] = 'upplen'

data.agg[sapply(data.agg['id'],function(x) x==0),'id'] = 'id0'
data.agg[sapply(data.agg['id'],function(x) x==1),'id'] = 'id1'
data.agg[sapply(data.agg['id'],function(x) x==2),'id'] = 'id2'
data.agg[sapply(data.agg['id'],function(x) x==3),'id'] = 'id3'
data.agg[sapply(data.agg['id'],function(x) x==4),'id'] = 'id4'
data.agg[sapply(data.agg['id'],function(x) x==5),'id'] = 'id5'
data.agg[sapply(data.agg['id'],function(x) x==6),'id'] = 'id6'
data.agg[sapply(data.agg['id'],function(x) x==7),'id'] = 'id7'
data.agg[sapply(data.agg['id'],function(x) x==8),'id'] = 'id8'
data.agg[sapply(data.agg['id'],function(x) x==9),'id'] = 'id9'

detach(data.all)

# one-way repeated measures anova on fov
#aov.fov=aov(tt~fov+Error(id/fov),data.agg)
#print(summary(aov.fov))
#boxplot(tt~fov,data=data.agg)


# one-way repeated measures anova on deadlen
#aov.deadlen = aov(tt ~deadlen+Error(id/deadlen),data.agg)
#print(summary(aov.deadlen))
boxplot(tt~deadlen,data=data.agg)



# two-way anova repeated measures on both
aov.two = aov(tt ~(fov*deadlen)+Error(id/(fov*deadlen)),data.agg)
print(summary(aov.two))
#attach(data.agg)
#interaction.plot(fov,deadlen, tt)    #another way to graph the interaction
#detach(data.agg)
#boxplot(tt ~fov*deadlen,data=data.agg)








# one-way repeated measures anova on precision~fov
#aov.fov=aov(precision~fov+Error(id/fov),data.all)
#print(summary(aov.fov))
#boxplot(recall~fov,data=data.all)


# one-way repeated measures anova on precision~latency
#aov.latency=aov(precision~latency+Error(id/latency),data.all)
#print(summary(aov.latency))
#boxplot(recall~latency,data=data.all)



# two-way anova repeated measures on precision~(fov*latency)
#aov.two = aov(precision~(fov*latency)+Error(id/(fov*latency)),data.all)
#print(summary(aov.two))
#boxplot(recall~fov*latency,data=data.all)
#attach(data.all)
#interaction.plot(fov,latency,precision)    #another way to graph the interaction
#detach(data.all)

