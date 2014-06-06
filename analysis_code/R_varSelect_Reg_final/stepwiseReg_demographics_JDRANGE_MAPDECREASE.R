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
names_jd_range <- names_jd_range[which(names_jd_range!="401-405.99")][-1] #remove HTN from list of JD_RANGES 
s_model_jd_range_features <- paste(names_jd_range, collapse="+")
s_model_all_features <- paste(c(s_model_BP_prior, s_model_data0_features, s_model_jd_range_features) , collapse="+")


#null model
model_MAP_DECREASE_0 <- glm(MAP_DECREASE~1, data_for_model_scaled , family = binomial)
#formulas for each feature set
formula <- paste(c("MAP_DECREASE", s_model_all_features), collapse="~")
formula_data0 <- paste(c("MAP_DECREASE", s_model_data0_features), collapse="~")
formula_JD_only <- paste(c("MAP_DECREASE", s_model_jd_range_features), collapse="~")

#updated models - all features
model_MAP_DECREASE_1 <- update(model_MAP_DECREASE_0, formula )
model_MAP_DECREASE_1_data0 <- update(model_MAP_DECREASE_0, formula_data0 )
model_MAP_DECREASE_1_JD_only <- update(model_MAP_DECREASE_0, formula_JD_only )

#formula for all features
(f <- as.formula(paste("~", s_model_all_features)))
(f_data0 <- as.formula(paste("~",  s_model_data0_features)))
(f_JD_only <- as.formula(paste("~", s_model_jd_range_features)))

#stepwise ADD
model_MAP_DECREASE_allfeatures <- step(model_MAP_DECREASE_0, scope=list(lower=~1, upper=f), direction="forward")  	
model_MAP_DECREASE_data0 <- step(model_MAP_DECREASE_0, scope=list(lower=~1, upper=f_data0), direction="forward")  	
model_MAP_DECREASE_JD_only <- step(model_MAP_DECREASE_0, scope=list(lower=~1, upper=f_JD_only), direction="forward")  	

## plot ROC and AUC
plot.new()
plot.roc(data_for_model_scaled$MAP_DECREASE, fitted(model_MAP_DECREASE_allfeatures), print.auc=TRUE,
													#arguments for CI
													ci=TRUE, boot.n=100, ci.alpha=0.95, stratified=FALSE)
plot.roc(data_for_model_scaled$MAP_DECREASE, fitted(model_MAP_DECREASE_data0), add = TRUE, col="blue", print.auc=TRUE, print.auc.y=0.45,ci=TRUE, boot.n=100, ci.alpha=0.95, stratified=FALSE)
plot.roc(data_for_model_scaled$MAP_DECREASE, fitted(model_MAP_DECREASE_JD_only), add = TRUE, col="red", print.auc=TRUE, print.auc.y=0.40,ci=TRUE, boot.n=100, ci.alpha=0.95, stratified=FALSE)


## Run cluster
source('cluster_MAPDECREASE.R')

## save the workspace
curr_date_time <- Sys.time()
workspace_filename <- paste(c("stepwiseReg_demographics_JDRANGE_MAPDECREASE", curr_date_time, ".RData"), collapse="_")
save.image(workspace_filename)

