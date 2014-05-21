##
## R CMD BATCH --slave stepwiseRegression.R

#wideScreen() #wide screen view

input_file = '../../../data/new_data_20140416/Data_curated_RC/df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.csv'

data <- read.table(input_file, header = T, sep=',')

test <- sample(1:202,150,replace=FALSE)


data0 <- with(data, data.frame(MEDIAN_MAP_CHANGE = MEDIAN_MAP_CHANGE,
      	 	    		MEDIAN_SYSTOLIC_CHANGE=MEDIAN_SYSTOLIC_CHANGE, 
				MEDIAN_DIASTOLIC_CHANGE=MEDIAN_DIASTOLIC_CHANGE, 
				MEDIAN_MAP_LOWER = MEDIAN_MAP_CHANGE  <
				SEX = SEX, ETHNICITY = ETHNICITY, RACE= RACE, 
				AGE_ENGAGE=AGE_ENGAGE, AVG_BMI=AVG_BMI, 
				change_BMI=change_BMI,MEAN_EGFR, change_EGFR ))

#change sex to binary numbers
data0['SEX'] = sapply(data0['SEX'],function(x) gsub("F",as.integer(0),x))
data0['SEX'] = sapply(data0['SEX'],function(x) gsub("M",as.integer(1),x))

#transform to numeric
data0 = transform(data0, SEX = as.numeric(SEX),
		 ETHNICITY = as.numeric(ETHNICITY),
		 RACE = as.numeric(RACE),
		 AGE_ENGAGE = as.numeric(AGE_ENGAGE),
		 AVG_BMI = as.numeric(AVG_BMI),
		 change_BMI = as.numeric(change_BMI),
		 MEAN_EGFR = as.numeric(MEAN_EGFR),
		 change_EGFR = as.numeric(change_EGFR)
		      )	     

#scale data
data0 <- as.data.frame(scale(data0))
data0_removeMissing <- na.omit(data0)      

#model
model0 <- glm(MEDIAN_DIASTOLIC_CHANGE~1, data0_removeMissing , family = binomial(logit))
model1 <- update(model0, MEDIAN_DIASTOLIC_CHANGE ~ SEX + ETHNICITY + RACE + AGE_ENGAGE + AVG_BMI + change_BMI + MEAN_EGFR + change_EGFR)
(f <- as.formula(paste("~", paste(names(coef(model1))[-1], collapse="+"))))
print( step(model0, scope=list(lower=~1, upper=f), direction="forward")  )

