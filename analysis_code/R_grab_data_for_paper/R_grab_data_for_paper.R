## grab data for the paper

## TABLE 1 - basic info on # of subjects
load("cluster_MAP_DECREASE_2.RData")

dim(data_for_model_not_scaled)
# this shows that there are 2556 individuals and 219 features used
#[1] 2521  232

dim(subset(data_for_model_not_scaled, DIABETES==1))
#[1] 892 232

dim(subset(data_for_model_not_scaled, CHF==1))
#[1] 213 219




#for calculating MEAN/PERCENTILE of before/after BP's - ALL pts
mean(data_for_model_not_scaled$SYSTOLIC_BEFORE)
mean(data_for_model_not_scaled$DIASTOLIC_BEFORE)
mean(data_for_model_not_scaled$MAP_BEFORE)
mean(data_for_model_not_scaled$SYSTOLIC_AFTER)
mean(data_for_model_not_scaled$DIASTOLIC_AFTER)
mean(data_for_model_not_scaled$MAP_AFTER)
mean(data_for_model_not_scaled$SYSTOLIC_CHANGE)
mean(data_for_model_not_scaled$DIASTOLIC_CHANGE)
mean(data_for_model_not_scaled$MAP_CHANGE)

quantile(data_for_model_not_scaled$SYSTOLIC_BEFORE, c(0.25, 0.75))
quantile(data_for_model_not_scaled$DIASTOLIC_BEFORE, c(0.25, 0.75))
quantile(data_for_model_not_scaled$MAP_BEFORE, c(0.25, 0.75))
quantile(data_for_model_not_scaled$SYSTOLIC_AFTER, c(0.25, 0.75))
quantile(data_for_model_not_scaled$DIASTOLIC_AFTER, c(0.25, 0.75))
quantile(data_for_model_not_scaled$MAP_AFTER, c(0.25, 0.75))
quantile(data_for_model_not_scaled$SYSTOLIC_CHANGE, c(0.25, 0.75))
quantile(data_for_model_not_scaled$DIASTOLIC_CHANGE, c(0.25, 0.75))
quantile(data_for_model_not_scaled$MAP_CHANGE, c(0.25, 0.75))

#for calculating MEAN/PERCENTILE of before/after BP's - DIABETES pts
mean(subset(data_for_model_not_scaled, DIABETES==1)$SYSTOLIC_BEFORE)
mean(subset(data_for_model_not_scaled, DIABETES==1)$DIASTOLIC_BEFORE)
mean(subset(data_for_model_not_scaled, DIABETES==1)$MAP_BEFORE)
mean(subset(data_for_model_not_scaled, DIABETES==1)$SYSTOLIC_AFTER)
mean(subset(data_for_model_not_scaled, DIABETES==1)$DIASTOLIC_AFTER)
mean(subset(data_for_model_not_scaled, DIABETES==1)$MAP_AFTER)
mean(subset(data_for_model_not_scaled, DIABETES==1)$SYSTOLIC_CHANGE)
mean(subset(data_for_model_not_scaled, DIABETES==1)$DIASTOLIC_CHANGE)
mean(subset(data_for_model_not_scaled, DIABETES==1)$MAP_CHANGE)

quantile(subset(data_for_model_not_scaled, DIABETES==1)$SYSTOLIC_BEFORE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, DIABETES==1)$DIASTOLIC_BEFORE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, DIABETES==1)$MAP_BEFORE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, DIABETES==1)$SYSTOLIC_AFTER, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, DIABETES==1)$DIASTOLIC_AFTER, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, DIABETES==1)$MAP_AFTER, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, DIABETES==1)$SYSTOLIC_CHANGE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, DIABETES==1)$DIASTOLIC_CHANGE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, DIABETES==1)$MAP_CHANGE, c(0.25, 0.75))

#for calculating MEAN/PERCENTILE of before/after BP's - CHF pts
mean(subset(data_for_model_not_scaled, CHF==1)$SYSTOLIC_BEFORE)
mean(subset(data_for_model_not_scaled, CHF==1)$DIASTOLIC_BEFORE)
mean(subset(data_for_model_not_scaled, CHF==1)$MAP_BEFORE)
mean(subset(data_for_model_not_scaled, CHF==1)$SYSTOLIC_AFTER)
mean(subset(data_for_model_not_scaled, CHF==1)$DIASTOLIC_AFTER)
mean(subset(data_for_model_not_scaled, CHF==1)$MAP_AFTER)
mean(subset(data_for_model_not_scaled, CHF==1)$SYSTOLIC_CHANGE)
mean(subset(data_for_model_not_scaled, CHF==1)$DIASTOLIC_CHANGE)
mean(subset(data_for_model_not_scaled, CHF==1)$MAP_CHANGE)

quantile(subset(data_for_model_not_scaled, CHF==1)$SYSTOLIC_BEFORE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, CHF==1)$DIASTOLIC_BEFORE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, CHF==1)$MAP_BEFORE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, CHF==1)$SYSTOLIC_AFTER, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, CHF==1)$DIASTOLIC_AFTER, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, CHF==1)$MAP_AFTER, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, CHF==1)$SYSTOLIC_CHANGE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, CHF==1)$DIASTOLIC_CHANGE, c(0.25, 0.75))
quantile(subset(data_for_model_not_scaled, CHF==1)$MAP_CHANGE, c(0.25, 0.75))

## Run KS test for BP changes
##all pts
ks.test(data_for_model_not_scaled$SYSTOLIC_BEFORE, data_for_model_not_scaled$SYSTOLIC_AFTER)
ks.test(data_for_model_not_scaled$DIASTOLIC_BEFORE, data_for_model_not_scaled$DIASTOLIC_AFTER)
ks.test(data_for_model_not_scaled$MAP_BEFORE, data_for_model_not_scaled$MAP_AFTER)
##diabetes pts
ks.test(subset(data_for_model_not_scaled, DIABETES==1)$SYSTOLIC_BEFORE, subset(data_for_model_not_scaled, DIABETES==1)$SYSTOLIC_AFTER)
ks.test(subset(data_for_model_not_scaled, DIABETES==1)$DIASTOLIC_BEFORE, subset(data_for_model_not_scaled, DIABETES==1)$DIASTOLIC_AFTER)
ks.test(subset(data_for_model_not_scaled, DIABETES==1)$MAP_BEFORE, subset(data_for_model_not_scaled, DIABETES==1)$MAP_AFTER)
##chf pts
ks.test(subset(data_for_model_not_scaled, CHF==1)$SYSTOLIC_BEFORE, subset(data_for_model_not_scaled, CHF==1)$SYSTOLIC_AFTER)
ks.test(subset(data_for_model_not_scaled, CHF==1)$DIASTOLIC_BEFORE, subset(data_for_model_not_scaled, CHF==1)$DIASTOLIC_AFTER)
ks.test(subset(data_for_model_not_scaled, CHF==1)$MAP_BEFORE, subset(data_for_model_not_scaled, CHF==1)$MAP_AFTER)


## calculate how many in each group for MAGNITUDE of change (-2, no change, +2)
dim(subset(data_for_model_not_scaled, SYSTOLIC_CHANGE <= -2))
dim(subset(data_for_model_not_scaled, SYSTOLIC_CHANGE > -2 & SYSTOLIC_CHANGE < 2))
dim(subset(data_for_model_not_scaled, SYSTOLIC_CHANGE > 2))
dim(subset(data_for_model_not_scaled, DIASTOLIC_CHANGE <= -2))
dim(subset(data_for_model_not_scaled, DIASTOLIC_CHANGE > -2 & DIASTOLIC_CHANGE < 2))
dim(subset(data_for_model_not_scaled, DIASTOLIC_CHANGE > 2))
dim(subset(data_for_model_not_scaled, MAP_CHANGE <= -2))
dim(subset(data_for_model_not_scaled, MAP_CHANGE > -2 & MAP_CHANGE < 2))
dim(subset(data_for_model_not_scaled, MAP_CHANGE > 2))