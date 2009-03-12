datafilename="alldata.tab"
data.all=read.table(datafilename,header=T)	# read the data into a table

attach(data.all)
data.agg = aggregate(recall,list(fov,latency,id,gender,game), mean)
colnames(data.agg) <- c("fov","latency","id",'gender','game','recall')

#data.agg = aggregate(recall,list(fov,latency,id), mean)
#colnames(data.agg) <- c("fov","latency","id",'recall')

#data.agg = aggregate(ncorrect+nfalsepos,list(fov,latency,id), mean)
#colnames(data.agg) <- c("fov","latency","id",'nclicks')

#data.agg = aggregate((ncorrect+nfalsepos)/(ncorrect+nfalseneg),list(fov,latency,id), mean)
#colnames(data.agg) <- c("fov","latency","id",'click.ratio')

#data.agg = aggregate(nfalsepos+nfalseneg,list(fov,latency,id), mean)
#colnames(data.agg) <- c("fov","latency","id",'nerrors')

data.agg[sapply(data.agg['fov'],function(x) x==10),'fov'] = 'lowfov'
data.agg[sapply(data.agg['fov'],function(x) x==20),'fov'] = 'medfov'
data.agg[sapply(data.agg['fov'],function(x) x==34),'fov'] = 'uppfov'

data.agg[sapply(data.agg['latency'],function(x) x==1),'latency'] = 'lowlat'
data.agg[sapply(data.agg['latency'],function(x) x==6),'latency'] = 'medlat'
data.agg[sapply(data.agg['latency'],function(x) x==12),'latency'] = 'upplat'

data.agg[sapply(data.agg['id'],function(x) x==1),'id'] = 'id1'
data.agg[sapply(data.agg['id'],function(x) x==2),'id'] = 'id2'
data.agg[sapply(data.agg['id'],function(x) x==3),'id'] = 'id3'
data.agg[sapply(data.agg['id'],function(x) x==4),'id'] = 'id4'
data.agg[sapply(data.agg['id'],function(x) x==5),'id'] = 'id5'
data.agg[sapply(data.agg['id'],function(x) x==6),'id'] = 'id6'

data.agg[sapply(data.agg['game'],function(x) x==1),'game'] = '0-1'
data.agg[sapply(data.agg['game'],function(x) x==3),'game'] = '2-5'
data.agg[sapply(data.agg['game'],function(x) x==10),'game'] = '5-15'

#data.agg[4] = log(data.agg[4])
#data.agg[17,4] <- -2

detach(data.all)

aov.gender=aov(recall~gender,data.agg)
print(summary(aov.gender))
boxplot(recall~gender,data=data.agg)

aov.game=aov(recall~game,data.agg)
print(summary(aov.game))
boxplot(recall~game,data=data.agg)

# one-way repeated measures anova on fov
#aov.fov=aov(recall~fov+Error(id/fov),data.agg)
#print(summary(aov.fov))
#boxplot(recall~fov,data=data.agg)


# one-way repeated measures anova on latency
#aov.latency=aov(recall~latency+Error(id/latency),data.agg)
#print(summary(aov.latency))
#boxplot(recall~latency,data=data.agg)



# two-way anova repeated measures on both
aov.two = aov(precision ~(fov*latency)+Error(id/(fov*latency)),data.agg)
print(summary(aov.two))
#boxplot(precision ~fov*latency,data=data.agg)
attach(data.agg)
interaction.plot(fov,latency, precision)    #another way to graph the interaction
detach(data.agg)









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

