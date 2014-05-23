## Robert Chen
## Monday 5/12/2014
##
## compiling all relevant data for regression into one dataframe
## for ease of use in regression
##
## note: there are MISSING VALUES!!! <- needs further processing for analysis if using sklearn
##

output_dir = '../../data/new_data_20140416/Data_curated_RC/'

## build dataframes for BP before/after ####################################################################################

#predominant conrol status
df_BP_STATUS = pd.DataFrame(d_bp_status_pt_level_clinician.items(), columns=['RUID', 'BP_STATUS']) #predominant BP status
#Comorbidity (DM / CHF) status [whether or not they're being treated for it in the MHT program#
l_patients_DM = data_BP_stratComorbid['dm']['d_bp_before_after_MHT']['AFTER'].keys() #this gives the list of RUID's which are being tx for DM
l_patients_CHF = data_BP_stratComorbid['chf']['d_bp_before_after_MHT']['AFTER'].keys()
d_DM_status = dict(zip(l_patients_DM, [1]*len(l_patients_DM)))
d_CHF_status = dict(zip(l_patients_CHF, [1]*len(l_patients_CHF)))

#add DM/CHF binary status to BP_STATUS dataframe
df_DM_STATUS = pd.DataFrame( d_DM_status.items(), columns=['RUID', 'DM_TX'])
df_CHF_STATUS = pd.DataFrame( d_CHF_status.items(), columns=['RUID', 'CHF_TX'])
df_BP_STATUS = pd.merge(df_BP_STATUS, df_DM_STATUS, left_on='RUID', right_on='RUID', how='outer')
df_BP_STATUS = pd.merge(df_BP_STATUS, df_CHF_STATUS, left_on='RUID', right_on='RUID', how='outer')
df_BP_STATUS['DM_TX'] = df_BP_STATUS['DM_TX'].apply(lambda x: 1 if x==1 else 0)
df_BP_STATUS['CHF_TX'] = df_BP_STATUS['CHF_TX'].apply(lambda x: 1 if x==1 else 0)

#BP change before/after MHT engage date
d_BP_SYSTOLIC_BEFORE = dict()
d_BP_SYSTOLIC_AFTER = dict()
d_BP_DIASTOLIC_BEFORE = dict()
d_BP_DIASTOLIC_AFTER = dict()
d_BP_MAP_BEFORE = dict()
d_BP_MAP_AFTER = dict()
d_BP_SYSTOLIC_CHANGE = dict()
d_BP_DIASTOLIC_CHANGE = dict()
d_BP_MAP_CHANGE = dict()
for key in d_bp_before_after_MHT['BEFORE']:
    d_BP_SYSTOLIC_BEFORE[key] = d_bp_before_after_MHT['BEFORE'][key]['SYSTOLIC']
    d_BP_SYSTOLIC_AFTER[key] = d_bp_before_after_MHT['AFTER'][key]['SYSTOLIC']
    d_BP_DIASTOLIC_BEFORE[key] = d_bp_before_after_MHT['BEFORE'][key]['DIASTOLIC']
    d_BP_DIASTOLIC_AFTER[key] = d_bp_before_after_MHT['AFTER'][key]['DIASTOLIC']
    d_BP_MAP_BEFORE[key] = d_bp_before_after_MHT['BEFORE'][key]['MAP']
    d_BP_MAP_AFTER[key] = d_bp_before_after_MHT['AFTER'][key]['MAP']
    d_BP_SYSTOLIC_CHANGE[key] = d_BP_SYSTOLIC_AFTER[key] - d_BP_SYSTOLIC_BEFORE[key]
    d_BP_DIASTOLIC_CHANGE[key] = d_BP_DIASTOLIC_AFTER[key] - d_BP_DIASTOLIC_BEFORE[key]
    d_BP_MAP_CHANGE[key] = d_BP_MAP_AFTER[key] - d_BP_MAP_BEFORE[key]
    

df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.DataFrame(d_BP_SYSTOLIC_BEFORE.items(), columns=['RUID', 'MEDIAN_SYSTOLIC_BEFORE'])
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(d_BP_SYSTOLIC_AFTER.items(), columns=['RUID', 'MEDIAN_SYSTOLIC_AFTER']) ,left_on = 'RUID', right_on = 'RUID', how = 'outer')
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(d_BP_DIASTOLIC_BEFORE.items(), columns=['RUID', 'MEDIAN_DIASTOLIC_BEFORE']) ,left_on = 'RUID', right_on = 'RUID', how = 'outer')
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(d_BP_DIASTOLIC_AFTER.items(), columns=['RUID', 'MEDIAN_DIASTOLIC_AFTER']) ,left_on = 'RUID', right_on = 'RUID', how = 'outer')
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(d_BP_MAP_BEFORE.items(), columns=['RUID', 'MEDIAN_MAP_BEFORE']) ,left_on = 'RUID', right_on = 'RUID', how = 'outer')
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(d_BP_MAP_AFTER.items(), columns=['RUID', 'MEDIAN_MAP_AFTER']) ,left_on = 'RUID', right_on = 'RUID', how = 'outer')
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(d_BP_SYSTOLIC_CHANGE.items(), columns=['RUID', 'MEDIAN_SYSTOLIC_CHANGE']) ,left_on = 'RUID', right_on = 'RUID', how = 'outer')
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(d_BP_DIASTOLIC_CHANGE.items(), columns=['RUID', 'MEDIAN_DIASTOLIC_CHANGE']) ,left_on = 'RUID', right_on = 'RUID', how = 'outer') 
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(d_BP_MAP_CHANGE.items(), columns=['RUID', 'MEDIAN_MAP_CHANGE']) ,left_on = 'RUID', right_on = 'RUID', how = 'outer')
#add p-vals for KS test
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(ks_pvals_SYSTOLIC['HTN'].items(), columns=['RUID', 'P_KS_SYSTOLIC']), left_on = 'RUID', right_on = 'RUID', how = 'outer')
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(ks_pvals_DIASTOLIC['HTN'].items(), columns=['RUID', 'P_KS_DIASTOLIC']), left_on = 'RUID', right_on = 'RUID', how = 'outer')
df_BP_MEDIAN_BEFORE_AFTER_CHANGE = pd.merge(df_BP_MEDIAN_BEFORE_AFTER_CHANGE, pd.DataFrame(ks_pvals_MAP['HTN'].items(), columns=['RUID', 'P_KS_MAP']), left_on = 'RUID', right_on = 'RUID', how = 'outer')


## gather data for training examples / features ####################################################################################
#features for training examples 
df_Phenotype_BMI_ECG_EGFR = pd.merge(df_Phenotype, df_BMI_aggregate, left_on = 'RUID' , right_on = 'RUID', how = 'outer') #add Phenotype and BMI
df_Phenotype_BMI_ECG_EGFR = pd.merge(df_Phenotype_BMI_ECG_EGFR, df_ECG_aggregate, left_on = 'RUID' , right_on = 'RUID', how = 'outer') #add ECG
df_Phenotype_BMI_ECG_EGFR = pd.merge(df_Phenotype_BMI_ECG_EGFR, df_EGFR_aggregate, left_on = 'RUID' , right_on = 'RUID', how = 'outer') #add EGFR

# big dataframe with target clases ('BP_STATUS') and features for training examples
df_BPSTATUS_Phenotype_BMI_ECG_EGFR = pd.merge(df_BP_STATUS, df_Phenotype_BMI_ECG_EGFR, left_on = 'RUID', right_on='RUID', how = 'outer')

# big dataframe with BP's
df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE = pd.merge(df_BPSTATUS_Phenotype_BMI_ECG_EGFR, df_BP_MEDIAN_BEFORE_AFTER_CHANGE, left_on = 'RUID', right_on = 'RUID', how = 'outer')

#write file 
df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.to_csv( output_dir + 'df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.csv', index = False)

