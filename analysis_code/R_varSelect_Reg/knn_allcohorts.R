
#import library
library(class)

input_file = '../../../data/new_data_20140416/Data_curated_RC/df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.csv'

data <- read.table(input_file, header = T, sep=',')
#change sex to binary numbers
data['SEX'] = sapply(data['SEX'],function(x) gsub("F",as.integer(0),x))
data['SEX'] = sapply(data['SEX'],function(x) gsub("M",as.integer(1),x))

data0 <- with(data, data.frame(
      	 	    SYSTOLIC_CHANGE=MEDIAN_SYSTOLIC_CHANGE, 
				DIASTOLIC_CHANGE=MEDIAN_DIASTOLIC_CHANGE, 
				MAP_CHANGE = MEDIAN_MAP_CHANGE,
				SYSTOLIC_SIG_LOWER = KS_SYSTOLIC_SIG_LOWER,
				DIASTOLIC_SIG_LOWER = KS_DIASTOLIC_SIG_LOWER,
				MAP_SIG_LOWER = KS_MAP_SIG_LOWER,
				
				AGE=AGE_ENGAGE,
				SEX = SEX, 
				ETHNICITY_HISPANIC=ETHNICITY,
				RACE = RACE,
				WHITE=WHITE,
				BLACK=BLACK,
				ASIAN=ASIAN,
				HISPANIC=HISPANIC,
				BMI = AVG_BMI,
				change_BMI=change_BMI,
				EGFR = MEAN_EGFR, 
				change_EGFR = change_EGFR,
				DIABETES = DM_TX,
				CHF = CHF_TX,
				SYSTOLIC_BEFORE = MEDIAN_SYSTOLIC_BEFORE,
				SYSTOLIC_AFTER = MEDIAN_SYSTOLIC_AFTER,
				DIASTOLIC_BEFORE = MEDIAN_DIASTOLIC_BEFORE,
				DIASTOLIC_AFTER = MEDIAN_DIASTOLIC_AFTER,
				MAP_BEFORE = MEDIAN_MAP_BEFORE,
				MAP_AFTER = MEDIAN_MAP_AFTER
				))



#transform to numeric
data0 = transform(data0, 
		
      	SYSTOLIC_CHANGE=as.numeric(SYSTOLIC_CHANGE), 
		DIASTOLIC_CHANGE=as.numeric(DIASTOLIC_CHANGE), 
		MAP_CHANGE = as.numeric(MAP_CHANGE),
		SYSTOLIC_SIG_LOWER = as.factor(SYSTOLIC_SIG_LOWER),
		DIASTOLIC_SIG_LOWER = as.factor(DIASTOLIC_SIG_LOWER),
		MAP_SIG_LOWER = as.factor(MAP_SIG_LOWER),
		AGE=as.numeric(AGE),
		SEX = as.factor(SEX),
		ETHNICITY_HISPANIC = as.factor(ETHNICITY_HISPANIC),
		RACE = as.factor(RACE),
		WHITE=as.factor(WHITE),
		BLACK=as.factor(BLACK),
		ASIAN=as.factor(ASIAN),
		HISPANIC=as.factor(HISPANIC),
		BMI = as.numeric(BMI),
		change_BMI = as.numeric(change_BMI),
		EGFR = as.numeric(EGFR),
		change_EGFR = as.numeric(change_EGFR),
		DIABETES = as.factor(DIABETES),
		CHF = as.factor(CHF),
		SYSTOLIC_BEFORE = as.numeric(SYSTOLIC_BEFORE),
		SYSTOLIC_AFTER = as.numeric(SYSTOLIC_AFTER),
		DIASTOLIC_BEFORE = as.numeric(DIASTOLIC_BEFORE),
		DIASTOLIC_AFTER = as.numeric(DIASTOLIC_AFTER),
		MAP_BEFORE = as.numeric(MAP_BEFORE),
		MAP_AFTER = as.numeric(MAP_AFTER)
		)	     

#scale data
data0_removeMissing <- na.omit(data0) 
data0_model_features <- with(data0_removeMissing, data.frame(
		AGE=AGE,
		SEX = SEX,
		HISPANIC = ETHNICITY_HISPANIC,
		RACE = RACE,
		BMI = BMI,
		change_BMI = change_BMI,
		EGFR = EGFR,
		change_EGFR = change_EGFR,
		DIABETES = DIABETES,
		CHF = CHF
		)
	)

##KNN model
num_examples = dim(data0_model_features)[1] #number of total examples
train <-  data0_model_features[1: floor(num_examples/2), ]
test <- data0_model_features[ceiling(num_examples/2):num_examples, ]
train_labels <- data0_removeMissing$SYSTOLIC_SIG_LOWER[1: floor(num_examples/2)]
model_knn <- knn(train, test, train_labels, k = 10, l = 0, prob = FALSE, use.all = TRUE)




