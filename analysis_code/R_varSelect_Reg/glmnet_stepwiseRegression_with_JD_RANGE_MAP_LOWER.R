#glmnet_stepwiseRegression_with_JD_RANGE_MAP_LOWER.R
##
## R CMD BATCH --slave glmnet_stepwiseRegression_with_JD_RANGE_MAP_LOWER.R
## to combine a lot of columns into forumula, see: http://stackoverflow.com/questions/5251507/how-to-succinctly-write-a-formula-with-many-variables-from-a-data-frame
##

library(glmnet)
library(data.table)


########## LOAD DATA ###################################################################################################

input_file = '../../../data/new_data_20140416/Data_curated_RC/df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.csv'
icd_file = '../../../data/new_data_20140416/Data_curated_RC/df_ICD_counts.csv'
jd_file = '../../../data/new_data_20140416/Data_curated_RC/df_JD_counts.csv'
jd_range_file = '../../../data/new_data_20140416/Data_curated_RC/df_JD_RANGE_counts.csv'

data <- read.table(input_file, header = T, sep=',')
#data_icd <- read.table(icd_file, header = T, sep=',')
#data_jd <- read.table(jd_file, header = T, sep=',')
data_jd_range <- read.table(jd_range_file, header = T, sep=',')

#change sex to binary numbers
data['SEX'] = sapply(data['SEX'],function(x) gsub("F",as.integer(0),x))
data['SEX'] = sapply(data['SEX'],function(x) gsub("M",as.integer(1),x))

#replace missing values for icd_file with 0's
#data_icd[is.na(data_icd)] <- 0
data_jd_range[is.na(data_jd_range)] <- 0

data_continuous <- with(data, data.frame(
				RUID=RUID,
      	 	    SYSTOLIC_CHANGE=MEDIAN_SYSTOLIC_CHANGE, 
				DIASTOLIC_CHANGE=MEDIAN_DIASTOLIC_CHANGE, 
				MAP_CHANGE = MEDIAN_MAP_CHANGE,
				AGE=AGE_ENGAGE,
				BMI = AVG_BMI,
				change_BMI=change_BMI,
				EGFR = MEAN_EGFR, 
				change_EGFR = change_EGFR,
				SYSTOLIC_BEFORE = MEDIAN_SYSTOLIC_BEFORE,
				SYSTOLIC_AFTER = MEDIAN_SYSTOLIC_AFTER,
				DIASTOLIC_BEFORE = MEDIAN_DIASTOLIC_BEFORE,
				DIASTOLIC_AFTER = MEDIAN_DIASTOLIC_AFTER,
				MAP_BEFORE = MEDIAN_MAP_BEFORE,
				MAP_AFTER = MEDIAN_MAP_AFTER
				))

#isolate the binary features; because we won't scale them	
data0_binary = with(data, data.frame(
				RUID=RUID,
				SYSTOLIC_SIG_LOWER = KS_SYSTOLIC_SIG_LOWER,
				DIASTOLIC_SIG_LOWER = KS_DIASTOLIC_SIG_LOWER,
				MAP_SIG_LOWER = KS_MAP_SIG_LOWER,
				SEX = SEX,
				WHITE = WHITE,
				BLACK = BLACK,
				ASIAN = ASIAN, 
				HISPANIC = HISPANIC,
				DIABETES = DM_TX,
				CHF = CHF_TX
	))
data0_binary = transform(data0_binary, 
		SYSTOLIC_SIG_LOWER = as.numeric(SYSTOLIC_SIG_LOWER),
		DIASTOLIC_SIG_LOWER = as.numeric(DIASTOLIC_SIG_LOWER),
		MAP_SIG_LOWER = as.numeric(MAP_SIG_LOWER),
		SEX = as.factor(SEX),
		WHITE=as.factor(WHITE),
		BLACK=as.factor(BLACK),
		ASIAN=as.factor(ASIAN),
		HISPANIC=as.factor(HISPANIC),
		DIABETES = as.factor(DIABETES),
		CHF = as.factor(CHF)
	)


#transform to numeric
data0_continuous = transform(data_continuous, 
      	SYSTOLIC_CHANGE=as.numeric(SYSTOLIC_CHANGE), 
		DIASTOLIC_CHANGE=as.numeric(DIASTOLIC_CHANGE), 
		MAP_CHANGE = as.numeric(MAP_CHANGE),
		AGE=as.numeric(AGE),
		BMI = as.numeric(BMI),
		change_BMI = as.numeric(change_BMI),
		EGFR = as.numeric(EGFR),
		change_EGFR = as.numeric(change_EGFR),
		SYSTOLIC_BEFORE = as.numeric(SYSTOLIC_BEFORE),
		SYSTOLIC_AFTER = as.numeric(SYSTOLIC_AFTER),
		DIASTOLIC_BEFORE = as.numeric(DIASTOLIC_BEFORE),
		DIASTOLIC_AFTER = as.numeric(DIASTOLIC_AFTER),
		MAP_BEFORE = as.numeric(MAP_BEFORE),
		MAP_AFTER = as.numeric(MAP_AFTER)
		)  
##transform ICD columns to numeric
#cols = c(2:ncol(data_icd))
#data_icd[,cols] = apply(data_icd[,cols], 2, function(x) as.numeric(as.character(x)))
##transform JD_RANGE columns to numeric
cols = c(2:ncol(data_jd_range))
data_jd_range[,cols] = apply(data_jd_range[,cols], 2, function(x) as.numeric(as.character(x)))

#merge columns:
data0_as_datatable <- data.table::data.table(data0_continuous)
#data_icd_as_datatable <- data.table::data.table(data_icd)
data_jd_range_as_datatable <- data.table::data.table(data_jd_range)

##what data for the model?
#data_for_model <- merge(data0_as_datatable, data_icd_as_datatable, by = "RUID")
data_for_model_continuous <- as.data.frame(merge(data0_as_datatable, data_jd_range_as_datatable, by = "RUID"))


#scale data; but do NOT scale binary features
ruid_col = data_for_model["RUID"]
data_for_model_scaled <- data.frame(ruid_col,    scale(data_for_model_continuous[, -which(names(data_for_model_continuous) %in% c("RUID"))]))


##merge with binary features for BP change; binary features are NOT scaled
data_for_model_scaled <- merge(data0_binary, data_for_model_scaled, by="RUID")
#remove missing data (for the columns from data0)
data_for_model_scaled <- na.omit(data_for_model_scaled)
## NOT-scaled data:
data_for_model_not_scaled <- merge(data0_binary, data_for_model_continuous, by="RUID")
data_for_model_not_scaled <- na.omit(data_for_model_not_scaled)  


########## BUILD MODEL ###################################################################################################


## features as string
s_model_data0_features <- "AGE + SEX + WHITE + BLACK + ASIAN + HISPANIC + BMI + change_BMI + EGFR + change_EGFR + DIABETES + CHF"
#s_model_icd_features <- paste(colnames(data_icd_as_datatable)[2:length(colnames(data_icd_as_datatable))], collapse="+")
s_model_jd_range_features <- paste(colnames(data_jd_range_as_datatable)[2:length(colnames(data_jd_range_as_datatable))], collapse="+")
all_features <- paste(c(s_model_data0_features, s_model_jd_range_features) , collapse="+")

## this model
model_SYSTOLIC_0 <- glm(SYSTOLIC_CHANGE~1, data_for_model_scaled , family = gaussian)
model_DIASTOLIC_0 <- glm(DIASTOLIC_CHANGE~1, data_for_model_scaled , family = gaussian)
model_MAP_0 <- glm(MAP_CHANGE~1, data_for_model_scaled , family = gaussian)
model_SYSTOLIC_SIG_LOWER_0 <- glm(SYSTOLIC_SIG_LOWER~1, data_for_model_scaled , family = binomial)
model_DIASTOLIC_SIG_LOWER_0 <- glm(DIASTOLIC_SIG_LOWER~1, data_for_model_scaled , family = binomial)
model_MAP_SIG_LOWER_0 <- glm(MAP_SIG_LOWER~1, data_for_model_scaled , family = binomial)















