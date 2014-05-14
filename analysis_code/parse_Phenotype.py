## Robert Chen
## Monday 5/12/2014
##
## read and process Phenotype file
## this should be one line per patient, so no need to aggregate across lines
##
import datetime as dt

def convert_dtdays_to_years(x):
    if type(x) == dt.timedelta:
        return x.days/365.
    else:
        return x

## options
input_folder = '../../data/new_data_20140416/Data_20140409/'
output_dir = '../analysis_output/'

## Prepare data, read data
filename = input_folder + 'Phenotype_04082014.csv'
pd.set_option('display.line_width', 300)
df_Phenotype = pd.read_csv(filename)


## format dates
df_Phenotype['ENGAGE_DATE'] = pd.to_datetime(df_Phenotype['ENGAGE_DATE']).astype(dt.datetime)
df_Phenotype['ENROLL_DATE'] = pd.to_datetime(df_Phenotype['ENROLL_DATE']).astype(dt.datetime)
df_Phenotype['DOB'] = pd.to_datetime(df_Phenotype['DOB']).astype(dt.datetime)
df_Phenotype['DOD'] = pd.to_datetime(df_Phenotype['DOD']).astype(dt.datetime)


## new columns for age AT ENGAGE_DATE
df_Phenotype['AGE_ENGAGE'] = (df_Phenotype['ENGAGE_DATE'] - df_Phenotype['DOB']).astype(dt.timedelta)
df_Phenotype['AGE_DEATH'] = (df_Phenotype['DOD'] - df_Phenotype['DOB']).astype(dt.timedelta)
df_Phenotype['AGE_ENGAGE'] = df_Phenotype['AGE_ENGAGE'].apply(lambda x:  convert_dtdays_to_years(x) )
df_Phenotype['AGE_DEATH'] = df_Phenotype['AGE_DEATH'].apply(lambda x:  convert_dtdays_to_years(x) )



## plot ages
fig = plt.figure(1)
plt.hist(df_Phenotype['AGE_ENGAGE'], bins=100)
plt.xlabel('Age at MHT engage date')
plt.ylabel('# subjects')
savestr = output_dir + 'plot_hist_MHT_age_ENGAGE_DATE.png'
fig.savefig(savestr)
plt.close()
