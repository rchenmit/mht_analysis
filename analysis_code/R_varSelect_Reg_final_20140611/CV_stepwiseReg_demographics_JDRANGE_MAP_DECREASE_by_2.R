## libraries ##########
library(pROC)

## load data ##########
rm(list=ls()[-length(ls())])
source('../R_data_load/load_data.R')

## build model ########


## features as string
s_model_BP_prior <- "MAP_BEFORE"
s_model_data0_features <- "AGE + SEX + WHITE + BLACK + ASIAN + HISPANIC + BMI + change_BMI + EGFR + change_EGFR + DIABETES + CHF"
names_jd_range <- colnames(data_jd_range_as_datatable)
names_jd_range <- names_jd_range[which(names_jd_range!="X401.405.99")][-1] #remove HTN from list of JD_RANGES
names_meds <- colnames(data_meds_as_datatable)
s_model_meds_features <- paste(names_meds, collapse="+")
s_model_jd_range_features <- paste(names_jd_range, collapse="+")
s_model_all_features <- paste(c(s_model_BP_prior, s_model_data0_features, s_model_meds_features, s_model_jd_range_features) , collapse="+")

###########################################################################################
findZeroVarianceVars <- function(x) {
    out <- lapply(training_set, function(x) length(unique(x)))
    want <- which(!out > 1)
    unlist(want)
}
lappend <- function (lst, ...){
lst <- c(lst, list(...))
  return(lst)
}


l_auc_all_folds = c()
num_fold = 10
cases = subset(data_for_model_scaled, MAP_DECREASE_2==1)
controls = subset(data_for_model_scaled, MAP_DECREASE_2==0)
num_cases = dim(cases)[1]
num_controls = dim(controls)[1]
l_stepwise_features_used_per_fold = list()

for (i in 1:num_fold) {
	rm(model_MAP_DECREASE_2_0_train)
	rm(model_MAP_DECREASE_2_allfeatures_train)
	print(paste("start CV fold", i))
	cases_test_sample = sample(1:num_cases, floor(num_cases / num_fold))
	controls_test_sample = sample(1:num_controls, floor(num_controls / num_fold))
	cases_test = cases[cases_test_sample, ]
	controls_test = controls[controls_test_sample, ]
	cases_train= cases[-cases_test_sample,]
	controls_train = controls[-controls_test_sample,]
	training_set = merge(cases_train, controls_train, all=TRUE)
	testing_set = merge(cases_test, controls_test, all=TRUE)

	#remove zero-variance variables from training set! (should be in meds or JD_range)
	zero_variance_features = names(findZeroVarianceVars(training_set))
	training_set = training_set[,-which(names(training_set) %in% zero_variance_features)]
	testing_set = testing_set[,-which(names(testing_set) %in% zero_variance_features)]
	names_meds_to_use = setdiff(names_meds, zero_variance_features)
	names_jd_range_to_use = setdiff(names_jd_range, zero_variance_features)
	s_names_meds_to_use = paste(names_meds_to_use, collapse="+")
	s_names_jd_range_to_use = paste(names_jd_range_to_use, collapse="+")
	s_model_features_to_use <- paste(c(s_model_BP_prior, s_model_data0_features, s_names_meds_to_use, s_names_jd_range_to_use) , collapse="+")


	#TRAINING SET: null model
	model_MAP_DECREASE_2_0_train <- glm(MAP_DECREASE_2~1, training_set , family = binomial)
	#TRAINING SET: formulas for each feature set
	formula <- paste(c("MAP_DECREASE_2", s_model_features_to_use), collapse="~")
	#TRAINING SET: formula for all features
	(f <- as.formula(paste("~", s_model_features_to_use)))
	#TRAINING SET: stepwise ADD
	model_MAP_DECREASE_2_allfeatures_train <- step(model_MAP_DECREASE_2_0_train, scope=list(lower=~1, upper=f), direction="forward")  	

	#TESTING SET - fit the training set model to the TESTING set
	predictions_testing_set <- predict(model_MAP_DECREASE_2_allfeatures_train, newdata=testing_set, type="response")
	testing_set$predictions <- predictions_testing_set
	roc_this_fold <- roc(MAP_DECREASE_2 ~ predictions, data = testing_set)
	auc_this_fold <- roc_this_fold$auc
	l_auc_all_folds <- append(l_auc_all_folds, auc_this_fold)

	##list of features used this fold
	l_features_this_fold <- names(coefficients(model_MAP_DECREASE_2_allfeatures_train))[-1]
	l_stepwise_features_used_per_fold = lappend(l_stepwise_features_used_per_fold, l_features_this_fold)
}
############################################################################################

#mean_AUC
mean_AUC = mean(l_auc_all_folds)
print(mean_AUC)

#INTERSECT list of features used across all folds:
l_stepwise_features_used_unique = Reduce('intersect',l_stepwise_features_used_per_fold )


## plot ROC and AUC
#plot.new()
#plot.roc(data_for_model_scaled$MAP_DECREASE_2, fitted(model_MAP_DECREASE_2_allfeatures), print.auc=TRUE,
#													#arguments for CI
#													ci=TRUE, boot.n=100, ci.alpha=0.95, stratified=FALSE, col="blue")


## save the workspace
curr_date_time <- Sys.time()
workspace_filename <- paste(c("stepwiseReg_demographics_JDRANGE_MAP_DECREASE_by_2", curr_date_time, ".RData"), collapse="_")
save.image(workspace_filename)


## Run cluster
source('cluster_MAP_DECREASE_by_2.R')


