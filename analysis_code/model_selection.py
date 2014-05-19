## Robert Chen
## Monday 5/12/2014
##
## model selection for partitioning patients --> to predict whether or not the program worked
##
## note: change impute, change lasso code


## import
from sklearn import linear_model

## build dataframes for BP before/after
df_BP_before_after_chnage = pd.DataFrame(d_change_EGFR.items(), columns=['RUID', 'change_EGFR'])

## gather data for training examples / targets
#features for training examples 
df_Phenotype_BMI_ECG_EGFR = pd.merge(df_Phenotype, df_BMI_aggregate, left_on = 'RUID' , right_on = 'RUID', how = 'outer') #add Phenotype and BMI
df_Phenotype_BMI_ECG_EGFR = pd.merge(df_Phenotype_BMI_ECG_EGFR, df_ECG_aggregate, left_on = 'RUID' , right_on = 'RUID', how = 'outer') #add ECG
df_Phenotype_BMI_ECG_EGFR = pd.merge(df_Phenotype_BMI_ECG_EGFR, df_EGFR_aggregate, left_on = 'RUID' , right_on = 'RUID', how = 'outer') #add EGFR

#target classes
df_BP_STATUS = pd.DataFrame(d_bp_status_pt_level_clinician.items(), columns=['RUID', 'BP_STATUS'])
df_BP_STATUS['BP_STATUS'][df_BP_STATUS['BP_STATUS']== -1] = 0

# big dataframe with target clases ('BP_STATUS') and features for training examples
df_BPSTATUS_Phenotype_BMI_ECG_EGFR = pd.merge(df_BP_STATUS, df_Phenotype_BMI_ECG_EGFR, left_on = 'RUID', right_on='RUID', how = 'outer')


## impute missing values?? - CHANGE THIS!

## Run Lasso - CHANGE THIS!
clfLasso = linear_model.Lasso(alpha = 0.1)
l_subjects = []

df_subjects_features = df_BPSTATUS_Phenotype_BMI_ECG_EGFR.ix[:, ['BP_STATUS', 'ETHNICITY', 'RACE', 'AGE_ENGAGE', 'BMI', 'change_BMI']].dropna()
nparr_subjects = np.array(df_subjects_features.ix[:, ['ETHNICITY', 'RACE', 'AGE_ENGAGE', 'BMI', 'change_BMI']])
l_targets = list(df_subjects_features['BP_STATUS'])

## Run Lasso
clfLasso.fit(nparr_subjects, l_targets)
print clfLasso.coef_



