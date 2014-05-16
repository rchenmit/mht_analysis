## Robert Chen
## Monday 5/12/2014
##
## read and process BMI file
##
##
import datetime as dt

## options
input_folder = '../../data/new_data_20140416/Data_20140409/'

## Prepare data, read data
filename = input_folder + 'ECG_04082014.csv'
pd.set_option('display.line_width', 300)
df_ECG = pd.read_csv(filename, sep='|')
df_ECG['ECG_DATE'] = pd.to_datetime(df_ECG['ECG_DATE'])

## aggregate ECG numbers
df_ECG_aggregate = df_ECG.groupby(df_ECG.RUID).mean()


## calculate other features (that can't be averaged bc they're not numbers): change in BMI, pregnancy before/after
d_change_ECG = dict()


for ruid in df_ECG_aggregate.index:
    date_mht_engage = df_Phenotype[df_Phenotype.RUID == ruid]['ENGAGE_DATE'].astype(dt.datetime).values[0]
    date_2_yr_before = date_mht_engage - dt.timedelta(360*2)
    df_this_pt = df_ECG[df_ECG['RUID']==ruid]
    df_this_pt = df_this_pt.sort('ECG_DATE')
    condition_before_time_window = (df_this_pt['ECG_DATE'] < date_mht_engage) &  (df_this_pt['ECG_DATE']> date_2_yr_before)
    condition_after_time_window = (df_this_pt['ECG_DATE'] > date_mht_engage) 
        
    mean_ECG_before = np.mean(df_this_pt[condition_before_time_window][['RUID', 'PR_INTERVAL', 'QRS_DURATION', 'QT_INTERVAL', 'QT_INTERVAL_CORRECTED', 'HEAR_RATE_CORRECTED', 'P_WAVE', 'INITIAL_40_MS', 'MEAN_QRS', 'TERMINAL_40_MS', 'ST_SEGMENT', 'T_WAVE']], axis=0) if len(df_this_pt[condition_before_time_window])>0 else df_this_pt[['PR_INTERVAL', 'QRS_DURATION', 'QT_INTERVAL', 'QT_INTERVAL_CORRECTED', 'HEAR_RATE_CORRECTED', 'P_WAVE', 'INITIAL_40_MS', 'MEAN_QRS', 'TERMINAL_40_MS', 'ST_SEGMENT', 'T_WAVE']]*np.nan 
    mean_ECG_after = np.mean(df_this_pt[condition_after_time_window][['RUID', 'PR_INTERVAL', 'QRS_DURATION', 'QT_INTERVAL', 'QT_INTERVAL_CORRECTED', 'HEAR_RATE_CORRECTED', 'P_WAVE', 'INITIAL_40_MS', 'MEAN_QRS', 'TERMINAL_40_MS', 'ST_SEGMENT', 'T_WAVE']], axis=0) if len(df_this_pt[condition_after_time_window])>0 else df_this_pt[['PR_INTERVAL', 'QRS_DURATION', 'QT_INTERVAL', 'QT_INTERVAL_CORRECTED', 'HEAR_RATE_CORRECTED', 'P_WAVE', 'INITIAL_40_MS', 'MEAN_QRS', 'TERMINAL_40_MS', 'ST_SEGMENT', 'T_WAVE']]*np.nan
    mean_ECG_all = np.mean(df_this_pt[['RUID', 'PR_INTERVAL', 'QRS_DURATION', 'QT_INTERVAL', 'QT_INTERVAL_CORRECTED', 'HEAR_RATE_CORRECTED', 'P_WAVE', 'INITIAL_40_MS', 'MEAN_QRS', 'TERMINAL_40_MS', 'ST_SEGMENT', 'T_WAVE']], axis=0)



## join other features to aggreagate        
#df_BMI_aggregate = pd.merge( df_BMI_aggregate, pd.DataFrame(d_change_BMI.items(), columns=['RUID', 'change_BMI']) , how='outer')
#df_BMI_aggregate = pd.merge( df_BMI_aggregate, pd.DataFrame(d_pregnant_before.items(), columns=['RUID', 'pregnant_before']), how='outer')
#df_BMI_aggregate = pd.merge( df_BMI_aggregate, pd.DataFrame(d_pregnant_after.items(), columns=['RUID', 'pregnant_after']),  how='outer')

