## Robert Chen
## Monday 5/12/2014
##
## read and process BMI file
##
##
import datetime as dt

## options
input_folder = '../../data/new_data_20140416/Data_20140409/'
output_dir = '../../data/new_data_20140416/Data_curated_RC/'

## Prepare data, read data
filename = input_folder + 'ICD_9_04082014.csv'
pd.set_option('display.line_width', 300)
df_ICD = pd.read_csv(filename, sep=',')

df_ICD['EVENT_DATE'] = pd.to_datetime(df_ICD['EVENT_DATE'])


## make a counts matrix
unique_ICD_values = df_ICD.ICD_9_CODE.unique() #ARRAY with unique ICD codes as STRINGS
df_ICD_counts = pd.DataFrame(columns=['RUID'])
#for icd in unique_ICD_values:
#    if isinstance(icd, str):
#        if mod(len(df_ICD_counts.columns), 100) == 0:
#            print len(df_ICD_counts.columns)
#        df_this_icd = df_ICD[df_ICD.ICD_9_CODE==icd][['RUID', 'ICD_9_CODE']]
#        df_this_icd[icd] = df_this_icd.groupby('RUID').transform('count')
#        df_this_icd = df_this_icd.drop( 'ICD_9_CODE', 1)
#        df_this_icd = df_this_icd.drop_duplicates()
#        if len(df_ICD_counts) == 0:
#            df_ICD_counts = df_this_icd.copy()
#        else:
#            df_ICD_counts = pd.merge(df_ICD_counts, df_this_icd, left_on='RUID', right_on='RUID', how='outer')

for i in range(6148, len(unique_ICD_values)):
    icd = unique_ICD_values[i]
    if isinstance(icd, str):
        if mod(len(df_ICD_counts.columns), 100) == 0:
            print len(df_ICD_counts.columns)
        df_this_icd = df_ICD[df_ICD.ICD_9_CODE==icd][['RUID', 'ICD_9_CODE']]
        df_this_icd[icd] = df_this_icd.groupby('RUID').transform('count')
        df_this_icd = df_this_icd.drop( 'ICD_9_CODE', 1)
        df_this_icd = df_this_icd.drop_duplicates()
        if len(df_ICD_counts) == 0:
            df_ICD_counts = df_this_icd.copy()
        else:
            df_ICD_counts = pd.merge(df_ICD_counts, df_this_icd, left_on='RUID', right_on='RUID', how='outer')
        

with open(output_dir + "df_ICD_counts_fromCol6149.pickle", "wb") as output_file:
    pickle.dump(df_ICD_counts, output_file) 
output_file.close()

df_ICD_counts.to_csv( output_dir + 'df_ICD_counts_fromCol6149.csv', index = False)
