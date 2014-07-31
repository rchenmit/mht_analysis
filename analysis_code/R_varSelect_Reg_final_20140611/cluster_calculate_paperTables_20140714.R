rm(list=ls())
load("CV_stepwiseRegBIC_cluster_demographics_JDRANGE_MAP_DECREASE_by_2_1404068669.8946_.RData")
cluster_assignments = model_cluster$classification
data_merged_with_cluster = as.data.frame(merge(data_for_model_not_scaled, data.frame(model_cluster$classification), by=0))
data_merged_with_cluster_MAP = subset(data_merged_with_cluster, select =c("model_cluster.classification", "SYSTOLIC_BEFORE", "SYSTOLIC_AFTER", "SYSTOLIC_CHANGE", 
																										"DIASTOLIC_BEFORE", "DIASTOLIC_AFTER", "DIASTOLIC_CHANGE", 
																										"MAP_BEFORE", "MAP_AFTER", "MAP_CHANGE"))

# USE AGGREGATE FUNCTION
#
#> aggregate(data_merged_with_cluster_MAP, by=list(data_merged_with_cluster$model_cluster.classification), FUN=mean)
#  Group.1 model_cluster.classification SYSTOLIC_BEFORE SYSTOLIC_AFTER SYSTOLIC_CHANGE DIASTOLIC_BEFORE DIASTOLIC_AFTER DIASTOLIC_CHANGE MAP_BEFORE MAP_AFTER MAP_CHANGE
#1       1                            1        130.7107       129.8203      -0.8903948         74.30790        73.02298        -1.284915   93.16735  91.97947  -1.187881
#2       2                            2        133.8648       132.2730      -1.5918367         76.60587        74.64158        -1.964286   95.73257  93.87202  -1.860544
#3       3                            3        135.4730       134.4314      -1.0416667         71.97059        70.37990        -1.590686   93.28268  91.80556  -1.477124
#4       4                            4        130.6425       130.2675      -0.3750000         71.40570        70.24561        -1.160088   91.37061  90.31506  -1.055556


cluster1 = subset(data_merged_with_cluster, model_cluster.classification==1)
cluster2 = subset(data_merged_with_cluster, model_cluster.classification==2)
cluster3 = subset(data_merged_with_cluster, model_cluster.classification==3)
cluster4 = subset(data_merged_with_cluster, model_cluster.classification==4)

ks.test(cluster1$SYSTOLIC_BEFORE, cluster1$SYSTOLIC_AFTER)
ks.test(cluster1$DIASTOLIC_BEFORE, cluster1$DIASTOLIC_AFTER)
ks.test(cluster1$MAP_BEFORE, cluster1$MAP_AFTER)

ks.test(cluster2$SYSTOLIC_BEFORE, cluster2$SYSTOLIC_AFTER)
ks.test(cluster2$DIASTOLIC_BEFORE, cluster2$DIASTOLIC_AFTER)
ks.test(cluster2$MAP_BEFORE, cluster2$MAP_AFTER)

ks.test(cluster3$SYSTOLIC_BEFORE, cluster3$SYSTOLIC_AFTER)
ks.test(cluster3$DIASTOLIC_BEFORE, cluster3$DIASTOLIC_AFTER)
ks.test(cluster3$MAP_BEFORE, cluster3$MAP_AFTER)

ks.test(cluster4$SYSTOLIC_BEFORE, cluster4$SYSTOLIC_AFTER)
ks.test(cluster4$DIASTOLIC_BEFORE, cluster4$DIASTOLIC_AFTER)
ks.test(cluster4$MAP_BEFORE, cluster4$MAP_AFTER)


data_merged_with_cluster_MAP_decrease2 = subset(data_merged_with_cluster, MAP_CHANGE<=-2, select =c("model_cluster.classification", "MAP_DECREASE_2", "AGE", "SEX", "WHITE", "BLACK", "DIABETES", "CHF", "EGFR", "BMI"))
data_merged_with_cluster_MAP_nodecrease2 = subset(data_merged_with_cluster, MAP_CHANGE>-2, select =c("model_cluster.classification", "MAP_DECREASE_2", "AGE", "SEX", "WHITE", "BLACK", "DIABETES", "CHF", "EGFR", "BMI"))


#> aggregate(data_merged_with_cluster_MAP_decrease2, by=list(data_merged_with_cluster_MAP_decrease2$model_cluster.classification), FUN=mean)
#  Group.1 model_cluster.classification MAP_DECREASE_2      AGE SEX WHITE BLACK DIABETES CHF     EGFR      BMI
#1       1                            1             NA 67.73687  NA    NA    NA       NA  NA 79.99784 53.89032
#2       2                            2             NA 62.87016  NA    NA    NA       NA  NA 84.94091 52.84915
#3       3                            3             NA 71.44356  NA    NA    NA       NA  NA 68.31983 48.97720
#4       4                            4             NA 68.83559  NA    NA    NA       NA  NA 73.22861 32.13380
#> aggregate(data_merged_with_cluster_MAP_nodecrease2, by=list(data_merged_with_cluster_MAP_nodecrease2$model_cluster.classification), FUN=mean)
#  Group.1 model_cluster.classification MAP_DECREASE_2      AGE SEX WHITE BLACK DIABETES CHF     EGFR      BMI
#1       1                            1             NA 67.91681  NA    NA    NA       NA  NA 80.30645 47.37584
#2       2                            2             NA 63.53896  NA    NA    NA       NA  NA 83.29257 38.40844
#3       3                            3             NA 72.40231  NA    NA    NA       NA  NA 68.50027 59.78584
#4       4                            4             NA 70.93090  NA    NA    NA       NA  NA 68.52515 99.16213

table(subset(data_merged_with_cluster_MAP_decrease2, select=c("SEX")))
table(subset(data_merged_with_cluster_MAP_decrease2, select=c("WHITE")))
table(subset(data_merged_with_cluster_MAP_decrease2, select=c("BLACK")))
table(subset(data_merged_with_cluster_MAP_decrease2, select=c("DIABETES")))
table(subset(data_merged_with_cluster_MAP_decrease2, select=c("CHF")))

# table(subset(data_merged_with_cluster_MAP_decrease2, select=c("CHF")))
# > table(subset(data_merged_with_cluster_MAP_decrease2, select=c("SEX")))
#   0   1 
# 660 538 
# > table(subset(data_merged_with_cluster_MAP_decrease2, select=c("WHITE")))

#   0   1 
# 222 976 
# > table(subset(data_merged_with_cluster_MAP_decrease2, select=c("BLACK")))

#   0   1 
# 992 206 
# > table(subset(data_merged_with_cluster_MAP_decrease2, select=c("DIABETES")))

#   0   1 
# 767 431 
# > table(subset(data_merged_with_cluster_MAP_decrease2, select=c("CHF")))

#    0    1 
# 1098  100

table(subset(data_merged_with_cluster_MAP_nodecrease2, select=c("SEX")))
table(subset(data_merged_with_cluster_MAP_nodecrease2, select=c("WHITE")))
table(subset(data_merged_with_cluster_MAP_nodecrease2, select=c("BLACK")))
table(subset(data_merged_with_cluster_MAP_nodecrease2, select=c("DIABETES")))
table(subset(data_merged_with_cluster_MAP_nodecrease2, select=c("CHF")))

## print out quantiles for BP changes: //added 7/22/2014
quantile(data_merged_with_cluster_MAP$SYSTOLIC_CHANGE, .05)
quantile(data_merged_with_cluster_MAP$SYSTOLIC_CHANGE, .95)
quantile(data_merged_with_cluster_MAP$DIASTOLIC_CHANGE, .05)
quantile(data_merged_with_cluster_MAP$DIASTOLIC_CHANGE, .95)
quantile(data_merged_with_cluster_MAP$MAP_CHANGE, .05)
quantile(data_merged_with_cluster_MAP$MAP_CHANGE, .95)

## calculate how many had change in MAP of at least -2mmHg
num_MAP_decrease_by_2 = dim(subset(data_merged_with_cluster, MAP_CHANGE<=-2))[1]
num_MAP_decrease = dim(subset(data_merged_with_cluster, MAP_CHANGE<=0))[1]
num_MAP_increase_by_2 = dim(subset(data_merged_with_cluster, MAP_CHANGE>2))[1]
num_MAP_increase = dim(subset(data_merged_with_cluster, MAP_CHANGE>0))[1]

#> num_MAP_decrease_by_2
#[1] 1198
#> num_MAP_decrease
#[1] 1481
#> num_MAP_increase_by_2
#[1] 789
#> num_MAP_increase
#[1] 1040
### percentage of pts with decrease in MAP
#> 1481/2521
#[1] 0.5874653

##############################################################################
#make scatterplot of before vs after MAP values
#
subset_MAP_decrease = subset(data_merged_with_cluster, MAP_CHANGE<=0)
subset_MAP_increase = subset(data_merged_with_cluster, MAP_CHANGE>0)
plot(subset_MAP_decrease$MAP_BEFORE, subset_MAP_decrease$MAP_AFTER, xlab="MAP before MHT program", ylab="MAP after MHT enrollment", xlim=c(65,140), ylim=c(65,140), col="green", pch=20, cex=0.9)
par(new=T) #acts like "hold on" in MATLAB
plot(subset_MAP_increase$MAP_BEFORE, subset_MAP_increase$MAP_AFTER, xlab="MAP before MHT program", ylab="MAP after MHT enrollment", xlim=c(65,140), ylim=c(65,140), col="red", pch=20, cex=0.9)
lines(c(50,160), c(50,160)) #to draw the line for increase vs decrease
#lines(c(50,160), c(52,162), lty=2) #for 2mmHg increase
#lines(c(50,160), c(48,158), lty=2) #for 2mmHg decrease
par(new=F)

##############################################################################
#make scatterplot of before vs after SBP values
#
subset_SYSTOLIC_decrease = subset(data_merged_with_cluster, SYSTOLIC_CHANGE<=0)
subset_SYSTOLIC_increase = subset(data_merged_with_cluster, SYSTOLIC_CHANGE>0)
plot(subset_SYSTOLIC_decrease$SYSTOLIC_BEFORE, subset_SYSTOLIC_decrease$SYSTOLIC_AFTER, xlab="SBP before MHT program", ylab="SBP after MHT enrollment", xlim=c(65,220), ylim=c(65,220), col="green", pch=20, cex=0.9)
par(new=T) #acts like "hold on" in MATLAB
plot(subset_SYSTOLIC_increase$SYSTOLIC_BEFORE, subset_SYSTOLIC_increase$SYSTOLIC_AFTER, xlab="SBP before MHT program", ylab="SBP after MHT enrollment", xlim=c(65,220), ylim=c(65,220), col="red", pch=20, cex=0.9)
lines(c(50,300), c(50,300)) #to draw the line for increase vs decrease
#lines(c(50,160), c(52,162), lty=2) #for 2mmHg increase
#lines(c(50,160), c(48,158), lty=2) #for 2mmHg decrease
par(new=F)


##############################################################################
#make scatterplot of before vs after DIASTOLIC values
#
subset_DIASTOLIC_decrease = subset(data_merged_with_cluster, DIASTOLIC_CHANGE<=0)
subset_DIASTOLIC_increase = subset(data_merged_with_cluster, DIASTOLIC_CHANGE>0)
plot(subset_DIASTOLIC_decrease$DIASTOLIC_BEFORE, subset_DIASTOLIC_decrease$DIASTOLIC_AFTER, xlab="DBP before MHT program", ylab="DBP after MHT enrollment", xlim=c(65,140), ylim=c(65,140), col="green", pch=20, cex=0.9)
par(new=T) #acts like "hold on" in MATLAB
plot(subset_DIASTOLIC_increase$DIASTOLIC_BEFORE, subset_DIASTOLIC_increase$DIASTOLIC_AFTER, xlab="DBP before MHT program", ylab="DBP after MHT enrollment", xlim=c(65,140), ylim=c(65,140), col="red", pch=20, cex=0.9)
lines(c(50,160), c(50,160)) #to draw the line for increase vs decrease
#lines(c(50,160), c(52,162), lty=2) #for 2mmHg increase
#lines(c(50,160), c(48,158), lty=2) #for 2mmHg decrease
par(new=F)