##
## R CMD BATCH --slave stepwiseRegression.R
## to combine a lot of columns into forumula, see: http://stackoverflow.com/questions/5251507/how-to-succinctly-write-a-formula-with-many-variables-from-a-data-frame
##

library(data.table)
library(pROC)


input_file = '../../../data/new_data_20140416/Data_curated_RC/df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.csv'
icd_file = '../../../data/new_data_20140416/Data_curated_RC/df_ICD_counts.csv'
jd_file = '../../../data/new_data_20140416/Data_curated_RC/df_JD_counts.csv'
jd_range_file = '../../../data/new_data_20140416/Data_curated_RC/df_JD_RANGE_counts.csv'
meds_file = '../../../data/new_data_20140416/Data_curated_RC/df_MEDS_HTN_counts.csv'


data <- read.table(input_file, header = T, sep=',')
#data_icd <- read.table(icd_file, header = T, sep=',')
#data_jd <- read.table(jd_file, header = T, sep=',')
data_jd_range <- read.table(jd_range_file, header = T, sep=',', check.names=TRUE)
data_meds <-read.table(meds_file, header=T, sep=',', check.names=TRUE)

#change sex to binary numbers
data['SEX'] = sapply(data['SEX'],function(x) gsub("F",as.integer(0),x))
data['SEX'] = sapply(data['SEX'],function(x) gsub("M",as.integer(1),x))
#BP improvement criteria
data['MAP_DECREASE_2'] = data$MEDIAN_MAP_CHANGE <= -2
data['MAP_INCREASE_2'] = data$MEDIAN_MAP_CHANGE <= -2
data['SYSTOLIC_OR_DIASTOLIC_DECREASE_2'] = data$MEDIAN_SYSTOLIC_CHANGE <= -2 | data$MEDIAN_DIASTOLIC_CHANGE <= -2

#replace missing values for icd_file with 0's
#data_icd[is.na(data_icd)] <- 0
data_jd_range[is.na(data_jd_range)] <- 0
data_meds[is.na(data_meds)] <- 0 

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
				SYSTOLIC_DECREASE = (MEDIAN_SYSTOLIC_CHANGE <0)*1,
				DIASTOLIC_DECREASE = (MEDIAN_DIASTOLIC_CHANGE <0)*1,
				MAP_DECREASE = (MEDIAN_MAP_CHANGE <0)*1,
				SYSTOLIC_SIG_LOWER = KS_SYSTOLIC_SIG_LOWER,
				DIASTOLIC_SIG_LOWER = KS_DIASTOLIC_SIG_LOWER,
				MAP_SIG_LOWER = KS_MAP_SIG_LOWER,
				SEX = SEX,
				WHITE = WHITE,
				BLACK = BLACK,
				ASIAN = ASIAN, 
				HISPANIC = HISPANIC,
				DIABETES = DM_TX,
				CHF = CHF_TX,
				MAP_DECREASE_2 = (MEDIAN_MAP_CHANGE <= -2)*1,
				MAP_INCREASE_2 = (MEDIAN_MAP_CHANGE >= 2)*1,
				SYSTOLIC_OR_DIASTOLIC_DECREASE_2 = (data$MEDIAN_SYSTOLIC_CHANGE <= -2 | data$MEDIAN_DIASTOLIC_CHANGE <= -2)*1
	))



data0_binary = transform(data0_binary,
		SYSTOLIC_DECREASE = as.factor(SYSTOLIC_DECREASE),
		DIASTOLIC_DECREASE = as.factor(DIASTOLIC_DECREASE),
		MAP_DECREASE =  as.factor(MAP_DECREASE),
		SYSTOLIC_SIG_LOWER = as.factor(SYSTOLIC_SIG_LOWER),
		DIASTOLIC_SIG_LOWER = as.factor(DIASTOLIC_SIG_LOWER),
		MAP_SIG_LOWER = as.factor(MAP_SIG_LOWER),
		SEX = as.factor(SEX),
		WHITE=as.factor(WHITE),
		BLACK=as.factor(BLACK),
		ASIAN=as.factor(ASIAN),
		HISPANIC=as.factor(HISPANIC),
		DIABETES = as.factor(DIABETES),
		CHF = as.factor(CHF),
		MAP_DECREASE_2 = as.factor(MAP_DECREASE_2),
		MAP_INCREASE_2 = as.factor(MAP_INCREASE_2),
		SYSTOLIC_OR_DIASTOLIC_DECREASE_2 = as.factor(SYSTOLIC_OR_DIASTOLIC_DECREASE_2)
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
data_jd_range_ruid = data_jd_range[2]
data_jd_range_counts = data_jd_range[-2] #RUID is 2nd column
data_jd_range_counts = apply(data_jd_range_counts[,], 2, function(x) as.numeric(as.character(x)))
data_jd_range_binary = as.data.frame(as.matrix( (data_jd_range_counts>0) + 0)) #make binary
data_jd_range_binary = apply(data_jd_range_binary[,], 2, function(x) as.factor(x))
df_jd_range_binary = data.frame(data_jd_range_ruid, data_jd_range_binary)

##transform MED columns to numeric
data_meds_ruid = data_meds[2]
data_meds_counts = data_meds[-2] #note: RUID is 2nd column in this case
data_meds_counts = apply(data_meds_counts[,], 2, function(x) as.numeric(as.character(x)))
data_meds_binary = as.data.frame(as.matrix( (data_meds_counts>0) + 0))
data_meds_binary = apply(data_meds_binary[,], 2, function(x) as.factor(x))
df_meds_binary = data.frame(data_meds_ruid, data_meds_binary)


#merge columns:
data0_as_datatable <- data.table::data.table(data0_continuous)
data_jd_range_as_datatable <- data.table::data.table(df_jd_range_binary)
data_meds_as_datatable <- data.table::data.table(df_meds_binary)

##what data for the model?
data_for_model_continuous <- as.data.frame(data0_as_datatable)

#scale data; but do NOT scale binary features
ruid_col = data_for_model_continuous["RUID"]
data_for_model_scaled <- data.frame(ruid_col,    scale(data_for_model_continuous[, -which(names(data_for_model_continuous) %in% c("RUID"))]))


##merge with binary features for BP change; binary features are NOT scaled
data_for_model_scaled <- merge(data0_binary, data_for_model_scaled, by="RUID")
data_for_model_scaled <- merge(data_for_model_scaled, data_jd_range_as_datatable, by="RUID")
data_for_model_scaled <- merge(data_for_model_scaled, data_meds_as_datatable, by="RUID")

#remove missing data (for the columns from data0)
data_for_model_scaled <- na.omit(data_for_model_scaled)  

## NOT-scaled data:
data_for_model_not_scaled <- merge(data0_binary, data_for_model_continuous, by="RUID")
data_for_model_not_scaled <- merge(data_for_model_not_scaled, data_jd_range_as_datatable, by="RUID")
data_for_model_not_scaled <- merge(data_for_model_not_scaled, data_meds_as_datatable, by="RUID")
data_for_model_not_scaled <- na.omit(data_for_model_not_scaled)