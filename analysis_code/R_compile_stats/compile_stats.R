library(matrixStats) #need this for colSds() function
library(foreach) #need this for foreach loop

## compiling status 

## input data
input_file = '../../../data/new_data_20140416/Data_curated_RC/df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.csv'

## read data
data_raw <- read.table(input_file, header = T, sep=',')
#remove missing data for ANY of the BP measurements
data <- subset( data_raw, !(is.na(MEDIAN_SYSTOLIC_BEFORE) | is.na(MEDIAN_SYSTOLIC_AFTER) | is.na(MEDIAN_DIASTOLIC_BEFORE) | is.na(MEDIAN_DIASTOLIC_AFTER) | is.na(MEDIAN_MAP_BEFORE) | is.na(MEDIAN_MAP_AFTER)  ))
print("num patients total, num features total; -- after disregarding patients that dont have BP's BEFORE and AFTER")
print(dim(data))

## functions
fillNAmedian=function(x){
    x<-as.numeric(as.character(x)) #first convert each column into numeric if it is from factor
    x[is.na(x)] =median(x, na.rm=TRUE) #convert the item with NA to median value from the column
    x #display the column
}

fillNAmean=function(x){
    x<-as.numeric(as.character(x)) #first convert each column into numeric if it is from factor
    x[is.na(x)] =median(x, na.rm=TRUE) #convert the item with NA to median value from the column
    x #display the column
}

## calculate stuff 
data_fill_NA_median = data.frame(apply(data,2,fillNAmedian))
data_fill_NA_mean   = data.frame(apply(data,2,fillNAmean))

#data_HTN_IC = subset(data_fill_NA_mean, BP_STATUS==1)
#data_HTN_OOC = subset(data_fill_NA_mean, BP_STATUS == -1)
#data_DM_IC = subset(data_fill_NA_mean, BP_STATUS == 1 & DM_TX ==1) 
#data_DM_OOC = subset(data_fill_NA_mean, BP_STATUS == -1 & DM_TX ==1) 
#data_CHF_IC = subset(data_fill_NA_mean, BP_STATUS == 1 & CHF_TX ==1) 
#data_CHF_OOC = subset(data_fill_NA_mean, BP_STATUS == -1 & CHF_TX ==1) 


data_HTN_IC = subset(data, BP_STATUS==1)
data_HTN_OOC = subset(data, BP_STATUS == -1)
data_DM_IC = subset(data, BP_STATUS == 1 & DM_TX ==1) 
data_DM_OOC = subset(data, BP_STATUS == -1 & DM_TX ==1) 
data_DM_ALL = subset(data, DM_TX ==1) 
data_CHF_IC = subset(data, BP_STATUS == 1 & CHF_TX ==1) 
data_CHF_OOC = subset(data, BP_STATUS == -1 & CHF_TX ==1) 
data_CHF_ALL = subset(data, CHF_TX ==1) 

## print the MEANS for for vitals/BP, by disease cluster
print("Print MEANS: -----------------------------------------------------------------------------------------------------------------------------------")
print(paste("HTN", "n_IC: ", dim(data_HTN_IC)[1], "n_OOC: ", dim(data_HTN_OOC)[1], "n_ALL: ", dim(data[1])))
print ( colMeans(data_HTN_IC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colMeans(data_HTN_OOC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colMeans(data[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))

print(paste("DM", "n_IC: ", dim(data_DM_IC)[1], "n_OOC: ", dim(data_DM_OOC)[1], "n_ALL: ", dim(data_DM_ALL[1])))
print ( colMeans(data_DM_IC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colMeans(data_DM_OOC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colMeans(data_DM_ALL[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))

print(paste("CHF", "n_IC: ", dim(data_CHF_IC)[1], "n_OOC: ", dim(data_CHF_OOC)[1], "n_ALL: ", dim(data_CHF_ALL[1])))
print ( colMeans(data_CHF_IC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colMeans(data_CHF_OOC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colMeans(data_CHF_ALL[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))


## print the SD's for vitals/BP, by disease cluster
print("Print STANDARD DEVIATIONS: ------------------------------------------------------------------------------------------------------------------------")
print(paste("HTN", "n_IC: ", dim(data_HTN_IC)[1], "n_OOC: ", dim(data_HTN_OOC)[1], "n_ALL: ", dim(data[1])))
print ( colSds(data_HTN_IC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colSds(data_HTN_OOC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colSds(data[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))

print(paste("DM", "n_IC: ", dim(data_DM_IC)[1], "n_OOC: ", dim(data_DM_OOC)[1], "n_ALL: ", dim(data_DM_ALL[1])))
print ( colSds(data_DM_IC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colSds(data_DM_OOC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colSds(data_DM_ALL[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))

print(paste("CHF", "n_IC: ", dim(data_CHF_IC)[1], "n_OOC: ", dim(data_CHF_OOC)[1], "n_ALL: ", dim(data_CHF_ALL[1])))
print ( colSds(data_CHF_IC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colSds(data_CHF_OOC[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))
print ( colSds(data_CHF_ALL[c('RUID', 'ETHNICITY', 'RACE', 'AVG_BMI', 'MEAN_EGFR', 'change_EGFR', 'MEDIAN_SYSTOLIC_BEFORE', 'MEDIAN_SYSTOLIC_AFTER', 'MEDIAN_SYSTOLIC_CHANGE', 'MEDIAN_DIASTOLIC_BEFORE', 'MEDIAN_DIASTOLIC_AFTER', 'MEDIAN_DIASTOLIC_CHANGE', 'MEDIAN_MAP_BEFORE', 'MEDIAN_MAP_AFTER' , 'MEDIAN_MAP_CHANGE')] , na.rm=T))


## print stuff for demographics table (for paper)
features_to_print = c('AGE_ENGAGE', 'MEDIAN_SYSTOLIC_BEFORE','MEDIAN_DIASTOLIC_AFTER','MEDIAN_DIASTOLIC_AFTER')
feature = 'AGE_ENGAGE'
label = "Age, years"
cat(paste(paste(label, paste(round(colMeans(data_HTN_IC[feature]),2),"\u00B1",round(colSds(data_HTN_IC[feature]),2), sep=''), paste(round(colMeans(data_HTN_OOC[feature]),2),"\u00B1",round(colSds(data_HTN_OOC[feature]),2), sep=''), sep="\t") , '\n'))

# categorical variables
feature = 'SEX'
label = "Sex"
indicator = "F"
cat(paste(paste(label, paste(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))," (",round(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))[1]/dim(data_HTN_IC)[1]*100,0), "%) female", sep=''), paste(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))," (",round(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))[1]/dim(data_HTN_OOC)[1]*100,0), "%) female", sep=''), sep="\t") , '\n'))
feature = 'RACE'
label = "white"
indicator = 3
cat(paste(paste(label, paste(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))," (",round(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))[1]/dim(data_HTN_IC)[1]*100,0), "%) white", sep=''), paste(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))," (",round(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))[1]/dim(data_HTN_OOC)[1]*100,0), "%) white", sep=''), sep="\t") , '\n'))
label = "black"
indicator = 0
cat(paste(paste(label, paste(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))," (",round(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))[1]/dim(data_HTN_IC)[1]*100,0), "%) black", sep=''), paste(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))," (",round(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))[1]/dim(data_HTN_OOC)[1]*100,0), "%) black", sep=''), sep="\t") , '\n'))
feature = 'DM_TX'
label = "Diabetes"
indicator = 1
cat(paste(paste(label, paste(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))," (",round(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))[1]/dim(data_HTN_IC)[1]*100,0), "%)", sep=''), paste(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))," (",round(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))[1]/dim(data_HTN_OOC)[1]*100,0), "%)", sep=''), sep="\t") , '\n'))
feature = 'CHF_TX'
label = "CHF"
indicator = 1
cat(paste(paste(label, paste(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))," (",round(dim(subset(data_HTN_IC, data_HTN_IC[feature]==indicator))[1]/dim(data_HTN_IC)[1]*100,0), "%)", sep=''), paste(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))," (",round(dim(subset(data_HTN_OOC, data_HTN_OOC[feature]==indicator))[1]/dim(data_HTN_OOC)[1]*100,0), "%)", sep=''), sep="\t") , '\n'))

# continuous variables 
feature = 'AVG_BMI'
label = "BMI"
cat(paste(paste(label, paste(round(colMeans(data_HTN_IC[feature], na.rm=T),2),"\u00B1",round(colSds(data_HTN_IC[feature],na.rm=T),2), sep=''), paste(round(colMeans(data_HTN_OOC[feature],na.rm=T),2),"\u00B1",round(colSds(data_HTN_OOC[feature],na.rm=T),2), sep=''), sep="\t") , '\n'))
feature = 'MEAN_EGFR'
label = "EGFR"
cat(paste(paste(label, paste(round(colMeans(data_HTN_IC[feature], na.rm=T),2),"\u00B1",round(colSds(data_HTN_IC[feature], na.rm=T),2), sep=''), paste(round(colMeans(data_HTN_OOC[feature], na.rm=T),2),"\u00B1",round(colSds(data_HTN_OOC[feature],na.rm=T),2), sep=''), sep="\t") , '\n'))
feature = 'MEDIAN_SYSTOLIC_BEFORE'
label = "SBP before MHT initiation"
cat(paste(paste(label, paste(round(colMeans(data_HTN_IC[feature]),2),"\u00B1",round(colSds(data_HTN_IC[feature]),2), sep=''), paste(round(colMeans(data_HTN_OOC[feature]),2),"\u00B1",round(colSds(data_HTN_OOC[feature]),2), sep=''), sep="\t") , '\n'))
feature = 'MEDIAN_SYSTOLIC_AFTER'
label = "SBP after MHT initiation"
cat(paste(paste(label, paste(round(colMeans(data_HTN_IC[feature]),2),"\u00B1",round(colSds(data_HTN_IC[feature]),2), sep=''), paste(round(colMeans(data_HTN_OOC[feature]),2),"\u00B1",round(colSds(data_HTN_OOC[feature]),2), sep=''), sep="\t") , '\n'))
feature = 'MEDIAN_DIASTOLIC_BEFORE'
label = "DBP before MHT initiation"
cat(paste(paste(label, paste(round(colMeans(data_HTN_IC[feature]),2),"\u00B1",round(colSds(data_HTN_IC[feature]),2), sep=''), paste(round(colMeans(data_HTN_OOC[feature]),2),"\u00B1",round(colSds(data_HTN_OOC[feature]),2), sep=''), sep="\t") , '\n'))
feature = 'MEDIAN_DIASTOLIC_AFTER'
label = "DBP after MHT initiation"
cat(paste(paste(label, paste(round(colMeans(data_HTN_IC[feature]),2),"\u00B1",round(colSds(data_HTN_IC[feature]),2), sep=''), paste(round(colMeans(data_HTN_OOC[feature]),2),"\u00B1",round(colSds(data_HTN_OOC[feature]),2), sep=''), sep="\t") , '\n'))





