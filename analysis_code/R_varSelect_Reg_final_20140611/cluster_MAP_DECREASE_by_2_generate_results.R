load("cluster_MAP_DECREASE_2.RData")


## overall demographics info
> dim(subset(data_merged_with_cluster, BLACK==1))
[1] 402 234
> dim(subset(data_merged_with_cluster, WHITE==1))
[1] 2087  234
> dim(subset(data_merged_with_cluster, WHITE==1 & CHF==1))
[1] 167 234
> dim(subset(data_merged_with_cluster, WHITE==1 & DIABETES==1))
[1] 680 234
> dim(subset(data_merged_with_cluster, BLACK==1 & CHF==1))
[1]  45 234
> dim(subset(data_merged_with_cluster, BLACK==1 & DIABETES==1))
[1] 203 234
> dim(subset(data_merged_with_cluster, SEX==1 & DIABETES==1))
[1] 447 234
> dim(subset(data_merged_with_cluster, SEX==1 & CHF==1))
[1] 108 234
> dim(subset(data_merged_with_cluster, SEX==1 ))
[1] 1135  234
> dim(subset(data_merged_with_cluster, DIABETES==1 ))
[1] 892 234
> dim(subset(data_merged_with_cluster, CHF==1 ))
[1] 213 234
> dim(subset(data_merged_with_cluster, DIABETES==1 & CHF==1))
[1] 103 234


## demogrpahics by cluster
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "X784.784.99"))))
#          X784.784.99
#cluster_id    0    1
#         1   18    0
#         2  327  139
#         3  216   90
#         5  144   36
#         6    0  330
#         7 1221    0
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "X617.629.99"))))
#           X617.629.99
# cluster_id    0    1
#          1   18    0
#          2   15  451
#          3  306    0
#          5  180    0
#          6  330    0
#          7 1221    0
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "ALDOSTERONE.ANTAGONISTS"))))
#           ALDOSTERONE.ANTAGONISTS
# cluster_id    0    1
#          1   14    4
#          2  403   63
#          3  238   68
#          5    0  180
#          6  330    0
#          7 1221    0
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "X226.227.99"))))
#           X226.227.99
# cluster_id    0    1
#          1   18    0
#          2  456   10
#          3  301    5
#          5  180    0
#          6  328    2
#          7 1219    2
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "X237.237.99"))))
#           X237.237.99
# cluster_id    0    1
#          1   18    0
#          2  447   19
#          3  306    0
#          5  180    0
#          6  330    0
#          7 1221    0
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "CENTRAL.ALPHA.AGONISTS"))))
#           CENTRAL.ALPHA.AGONISTS
# cluster_id    0    1
#          1   12    6
#          2  374   92
#          3    0  306
#          5  180    0
#          6  330    0
#          7 1221    0
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "X950.957.99"))))
#           X950.957.99
# cluster_id    0    1
#          1    0   18
#          2  460    6
#          3  306    0
#          5  180    0
#          6  330    0
#          7 1221    0

#for MEDIAN BMI
aggregate(subset(data_merged_with_cluster, select=c("BMI")), by=list(data_merged_with_cluster$cluster_id), FUN = median)
#  Group.1      BMI
#1       1 28.78340
#2       2 31.02265
#3       3 30.13980
#4       5 31.47893
#5       6 30.42048
#6       7 30.15714

aggregate(subset(data_merged_with_cluster, select=c("SYSTOLIC_CHANGE", "DIASTOLIC_CHANGE", "MAP_CHANGE")), by=list(data_merged_with_cluster$cluster_id), FUN = mean)
#  Group.1 SYSTOLIC_CHANGE DIASTOLIC_CHANGE  MAP_CHANGE
#1       1      -0.6388889        0.9166667  0.35185185
#2       2      -1.2510730       -1.8809013 -1.82081545
#3       3      -1.2026144       -1.4656863 -1.41938998
#4       5      -0.9222222       -1.4916667 -1.44629630
#5       6       0.7090909       -0.3378788 -0.03030303
#6       7      -1.2600328       -1.5159705 -1.42533443


## sort features by how many times they were used:
##function for appending lists
lappend <- function (lst, ...){
lst <- c(lst, list(...))
  return(lst)
}
l_allfeatures_allfolds_in_regression = c()
for (foldlist in l_stepwise_features_used_per_fold){
    l_allfeatures_allfolds_in_regression = c(l_allfeatures_allfolds_in_regression, as.vector(foldlist))
}

## print the occurrences for each cluster
df_clust_summary = data.frame()
for (clustername in names(table(data_merged_with_cluster$cluster_id)) )
{
    this_clust_summary = summary(subset(data_merged_with_cluster, cluster_id==clustername))[2, -c(1:2, 19:32)] #remove cols 1:2 ("Row.names" and "RUID") and 19:32 (continuous features)
    if (length(df_clust_summary) == 0){
        df_clust_summary = this_clust_summary
    } #base case
    else {
        df_clust_summary = data.frame(df_clust_summary, this_clust_summary)
    }
}
write.csv(df_clust_summary, quote=FALSE, file="cluster_features_counts_MAP_DECREASE_BY_2.csv")


## print the means for each cluster (continuous variables)
df_clust_continuous_means = aggregate(subset(data_merged_with_cluster, select=names(data_merged_with_cluster)[19:32] ), by=list(data_merged_with_cluster$cluster_id), FUN=mean)# columns 3 to 32 contain the continuous variables
write.csv(df_clust_continuous_means, quote=FALSE, row.names=FALSE, file="df_clust_summary_continuous_MEAN_20140619.csv")

## quantiles - by cluster
df_cluster_quantiles = data.frame()
for (clustername in names(table(data_merged_with_cluster$cluster_id)))
{
    quantiles_this_cluster = apply(subset(data_merged_with_cluster, cluster_id==clustername)[19:32], 2, quantile, probs = c(0.25, 0.75),  na.rm = TRUE)
    if (length(df_cluster_quantiles) == 0) {
        df_cluster_quantiles = data.frame(quantiles_this_cluster )
    }
    else {
        df_cluster_quantiles = rbind(df_cluster_quantiles, quantiles_this_cluster)
    }
}
write.csv(df_cluster_quantiles, quote=FALSE, row.names=FALSE, file="df_cluster_quantiles_continuousvars_20140619.csv")

## quantiles - by comorbidity
all_summary_counts = summary(subset(data_merged_with_cluster))[2, -c(1:2, 19:32)]
dm_summary_counts = summary(subset(data_merged_with_cluster, DIABETES==1))[2, -c(1:2, 19:32)]
chf_summary_counts = summary(subset(data_merged_with_cluster, CHF==1))[2, -c(1:2, 19:32)]
all_summary_means = colMeans(subset(data_merged_with_cluster, select=names(data_merged_with_cluster)[19:32] ))
dm_summary_means = colMeans(subset(data_merged_with_cluster, DIABETES==1, select=names(data_merged_with_cluster)[19:32] ))
chf_summary_means = colMeans(subset(data_merged_with_cluster, CHF==1, select=names(data_merged_with_cluster)[19:32] ))
all_summary_means = colMeans(subset(data_merged_with_cluster, select=names(data_merged_with_cluster)[19:32] ))
dm_summary_means = colMeans(subset(data_merged_with_cluster, DIABETES==1, select=names(data_merged_with_cluster)[19:32] ))
chf_summary_means = colMeans(subset(data_merged_with_cluster, CHF==1, select=names(data_merged_with_cluster)[19:32] ))
all_summary_quantiles = apply(subset(data_merged_with_cluster)[19:32], 2, quantile, probs = c(0.25, 0.75),  na.rm = TRUE)
dm_summary_quantiles = apply(subset(data_merged_with_cluster, DIABETES==1)[19:32], 2, quantile, probs = c(0.25, 0.75),  na.rm = TRUE)
chf_summary_quantiles = apply(subset(data_merged_with_cluster, CHF==1)[19:32], 2, quantile, probs = c(0.25, 0.75),  na.rm = TRUE)
all_median_BMI = median(subset(data_merged_with_cluster, select="BMI")$BMI)
dm_median_BMI = median(subset(data_merged_with_cluster, DIABETES ==1, select="BMI")$BMI)
chf_median_BMI = median(subset(data_merged_with_cluster, CHF ==1, select="BMI")$BMI)


#skew for continuous variables


#kurtosis for continuous variables




## print the medians for each cluster (continuous variables)
df_clust_continuous_medians = aggregate(subset(data_merged_with_cluster, select=names(data_merged_with_cluster)[19:32] ), by=list(data_merged_with_cluster$cluster_id), FUN=median)# columns 3 to 32 contain the continuous variables
write.csv(df_clust_continuous_medians, quote=FALSE, row.names=FALSE, file="df_clust_summary_continuous_MEDIAN_20140619.csv")



### 6/26/2014 - find 95% CI's
quantile(data_merged_with_cluster$SYSTOLIC_BEFORE, c(0.025, 0.975))
quantile(data_merged_with_cluster$SYSTOLIC_AFTER, c(0.025, 0.975))
quantile(data_merged_with_cluster$DIASTOLIC_BEFORE, c(0.025, 0.975))
quantile(data_merged_with_cluster$DIASTOLIC_AFTER, c(0.025, 0.975))
quantile(data_merged_with_cluster$MAP_BEFORE, c(0.025, 0.975))
quantile(data_merged_with_cluster$MAP_AFTER, c(0.025, 0.975))





