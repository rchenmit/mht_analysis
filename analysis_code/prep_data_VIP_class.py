## preparing example data for VIP class purposes
## use 30 pts with DM, and 30 overall from the entire dataset (there may be some overlap)

#output folder
output_dir = '../../VIP_sample_data/'

list1_DM = d_other_diag_clinician['dm'].keys()
list2_HTN = d_bp_clinician.keys()

diff = set(list2_HTN).difference( set(list1_DM)) 
diff = list(diff) #cast the set as a list

ruid_DM = list1_DM[0:15] #15 patients with DM
ruid_NO_DM = diff[0:15] #15 patients that do NOT have DM

all_sample_ruid = ruid_DM + ruid_NO_DM
all_sample_status = [1]*15 + [0]*15

#dataframes
df_sample_DM_status = pd.DataFrame( {'RUID' : all_sample_ruid ,
                                     'DIABETES_STATUS': all_sample_status } )
df_sample_EGFR_aggregate = df_EGFR_aggregate[df_EGFR_aggregate['RUID'].isin(all_sample_ruid)]
df_sample_BMI_aggregate = df_BMI_aggregate[df_BMI_aggregate['RUID'].isin(all_sample_ruid)]
df_sample_Phenotype = df_Phenotype[df_Phenotype['RUID'].isin(all_sample_ruid)]
df_sample_BP = df_BP[df_BP['RUID'].isin(all_sample_ruid)]
df_sample_ICD = df_ICD[df_ICD['RUID'].isin(all_sample_ruid)]
df_sample_CPT = df_CPT[df_CPT['RUID'].isin(all_sample_ruid)]
df_sample_LAB = df_LAB[df_LAB['RUID'].isin(all_sample_ruid)]

#write dataframes to CSV files
df_sample_DM_status.to_csv( output_dir + 'df_sample_DM_status.csv', index = False )
df_sample_EGFR_aggregate.to_csv( output_dir + 'df_sample_EGFR_aggregate.csv', index = False)
df_sample_BMI_aggregate.to_csv( output_dir + 'df_sample_BMI_aggregate.csv', index = False)
df_sample_Phenotype.to_csv( output_dir + 'df_sample_Phenotype.csv', index = False)
df_sample_BP.to_csv( output_dir + 'df_sample_BP.csv', index = False)
df_sample_ICD.to_csv( output_dir + 'df_sample_ICD.csv', index = False)
df_sample_CPT.to_csv( output_dir + 'df_sample_CPT.csv', index = False)
df_sample_LAB.to_csv( output_dir + 'df_sample_LAB.csv', index = False)
