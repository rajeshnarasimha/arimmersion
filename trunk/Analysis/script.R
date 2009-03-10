datafilename="alldata.tab"
data.all=read.table(datafilename,header=T)	# read the data into a table

aov.fov=aov(recall~condition+Error(id/condition),data.all)
print(summary(aov.fov))
boxplot(recall~condition,data=data.all)

aov.fov=aov(precision~condition+Error(id/condition),data.all)
print(summary(aov.fov))
boxplot(precision~condition,data=data.all)

# one-way repeated measures anova on fov
#aov.fov=aov(recall~fov+Error(id/fov),data.all)
#print(summary(aov.fov))
#boxplot(recall~fov,data=data.all)


# one-way repeated measures anova on latency
#aov.latency=aov(recall~latency+Error(id/latency),data.all)
#print(summary(aov.latency))
#boxplot(recall~latency,data=data.all)



# two-way anova repeated measures on both
aov.two = aov(recall~(fov*latency)+Error(id/(fov*latency)),data.all)
print(summary(aov.two))
#boxplot(recall~fov*latency,data=data.all)
attach(data.all)
interaction.plot(fov,latency,recall)    #another way to graph the interaction
detach(data.all)









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

