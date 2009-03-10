datafilename="alldata.csv"
data.all=read.csv(datafilename,header=T)	# read the data into a table

# one-way anova on fov
aov.fov=aov(percent_correct~fov,data.all)
print(summary(aov.fov))
#print(model.tables(aov.all,"means"),digits=3)
boxplot(percent_correct~fov,data=data.all)


# one-way anova on latency
aov.latency=aov(percent_correct~latency,data.all)
print(summary(aov.latency))
boxplot(percent_correct~latency,data=data.all)



# two-way anova on both
aov.two = aov(percent_correct~fov*latency,data.all)
print(summary(aov.two))
boxplot(percent_correct~fov*latency,data=data.all)


boxplot(percent_correct~fov/latency,data=data.all)