#cluster_MAPDECREASE.R
# do clustering with the features identified in stepwise regression

##cluster
library(mclust)
library(plyr)
names_cluster_features <- l_stepwise_features_used_unique
cluster_features <- data_for_model_scaled[, names_cluster_features]
model_cluster <- Mclust(cluster_features, G=1:40, modelNames=mclust.options("emModelNames"))
summary(model_cluster)
names(model_cluster)

model_predicted = as.data.frame(model_cluster$classification)
actual_targets = as.data.frame(data_for_model_scaled$SYSTOLIC_OR_DIASTOLIC_DECREASE_2)
predicted_actual <- data.frame(model_predicted, actual_targets)

#merge with original dataframe, for purpose of relevant things within clusters
data_merged_with_cluster <- as.data.frame( merge( data_for_model_not_scaled, data.frame(model_cluster$classification), by=0))
names(data_merged_with_cluster)[length(data_merged_with_cluster)] = "cluster_id"


#print cluster results
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "SEX"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "WHITE"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "DIABETES"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "CHF"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "SYSTOLIC_DECREASE"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "DIASTOLIC_DECREASE"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "MAP_DECREASE"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "MAP_DECREASE_2"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "MAP_INCREASE_2"))))
print(table(subset(data_merged_with_cluster, select=c("cluster_id", "SYSTOLIC_OR_DIASTOLIC_DECREASE_2"))))
aggregate(subset(data_merged_with_cluster, select=c("cluster_id", "AGE", "SYSTOLIC_BEFORE", "DIASTOLIC_BEFORE", "MAP_BEFORE", "SYSTOLIC_AFTER", "DIASTOLIC_AFTER", "MAP_AFTER", "BMI")), by = list(data_merged_with_cluster$cluster_id), FUN=mean)

# print average features
df_mean_features_by_cluster = aggregate(data_merged_with_cluster, by=list(data_merged_with_cluster$cluster_id), FUN=mean)
df_sum_features_by_cluster = ddply(data_merged_with_cluster,.(cluster_id), numcolwise(sum))
df_mean_sum_features_by_cluster = data.frame(df_mean_features_by_cluster, df_sum_features_by_cluster)
#WRONG NOW#df_5percentile_features_by_cluster = aggregate(data_merged_with_cluster, by=list(data_merged_with_cluster$cluster_id), FUN=mean)
#WRONG NOW#df_95percentile_features_by_cluster = aggregate(data_merged_with_cluster, by=list(data_merged_with_cluster$cluster_id), FUN=mean)
write.csv(df_mean_sum_features_by_cluster[, names_cluster_features], file="cluster_mean_sum_SYSTOLIC_OR_DIASTOLIC_DECREASE_2.csv")

save.image("cluster_SYSTOLIC_OR_DIASTOLIC_DECREASE_2.RData")


# print most common JD range codes
df_cluster_freq = as.data.frame(table(model_predicted))
df_cluster_jdrange_freq = df_cluster_freq
for (jdrange in names_jd_range) {
	df_this_jdrange = as.data.frame(table(subset(data_merged_with_cluster, select=c("cluster_id", jdrange))))
	df_this_jdrange_zero = subset(df_this_jdrange, eval(as.name(jdrange)) ==0)
	df_cluster_jdrange_freq[jdrange] = as.data.frame((df_cluster_freq$Freq - df_this_jdrange_zero$Freq) / df_cluster_freq$Freq )
}

cluster_names = as.numeric(df_cluster_freq$model_predicted)
for (cluster in cluster_names) {
	#print the top 10 JD ranges
	print(sort(subset(df_cluster_jdrange_freq, model_predicted==cluster), decreasing=T)[1:12])
}
