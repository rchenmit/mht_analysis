## compiling status 

## input data
input_file = '../../../data/new_data_20140416/Data_curated_RC/df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.csv'

## read data
data <- read.table(input_file, header = T, sep=',')

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

data_HTN_IC = 
data_HTN_OOC = 
data_DM_IC = 
data_DM_OOC = 
data_CHF_IC = 
data_CHF_OOC = 
