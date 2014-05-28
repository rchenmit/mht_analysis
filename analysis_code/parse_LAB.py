## Robert Chen
## Monday 5/12/2014
##
## read and process BMI file
##
##
import datetime as dt

## options
input_folder = '../../data/new_data_20140416/LAB_04082014/'
output_dir = '../../data/new_data_20140416/Data_curated_RC/'

## Prepare data, read data
filename = input_folder + 'LAB_04082014.csv'
pd.set_option('display.line_width', 300)
df_LAB = pd.read_csv(filename, sep=',' , escapechar='\\')

df_LAB['LAB_DATE'] = pd.to_datetime(df_LAB['LAB_DATE'])


## make a counts matrix
unique_LAB_names = df_LAB.LAB_NAME.unique() #ARRAY with unique ICD codes as STRINGS

df_LAB_counts = pd.DataFrame(columns=['RUID'])


###
##   CHANGE THE FOLLOWING CODE FOR LABS!  ##################################################################
#
#
#for icd in unique_ICD_values:
#    if isinstance(icd, str):
#        if mod(len(df_ICD_counts.columns), 100) == 0:
#            print len(df_ICD_counts.columns)
#        df_this_icd = df_ICD[df_ICD.ICD_9_CODE==icd][['RUID', 'ICD_9_CODE']]
#        df_this_icd[icd] = df_this_icd.groupby('RUID').transform('count')
#        df_this_icd = df_this_icd.drop( 'ICD_9_CODE', 1)
#        df_this_icd = df_this_icd.drop_duplicates()
#        df_this_icd.replace(np.nan, 0)
#        if len(df_ICD_counts) == 0:
#            df_ICD_counts = df_this_icd.copy()
#        else:
#            df_ICD_counts = pd.merge(df_ICD_counts, df_this_icd, left_on='RUID', right_on='RUID', how='outer')
#
#df_ICD_counts.to_csv( output_dir + 'df_ICD_counts.csv', index = False)
