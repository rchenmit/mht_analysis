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
filename = input_folder + 'EGFR_04082014.csv'
pd.set_option('display.line_width', 300)
df_EGFR = pd.read_csv(filename)

df_EGFR['LAB_DATE'] = pd.to_datetime(df_EGFR['LAB_DATE'])

df_EGFR_aggregate = df_EGFR.groupby(df_EGFR.RUID).mean()


## calculate other features (that can't be averaged bc they're not numbers): change in BMI, pregnancy before/after
d_change_EGFR = dict()

for ruid in df_EGFR_aggregate.index:
    if ruid in list(df_Phenotype.RUID): #they are in Phenotype.csv, meaning the MHT engage date is recorded for the pt
        date_mht_engage = df_Phenotype[df_Phenotype.RUID == ruid]['ENGAGE_DATE'].astype(dt.datetime).values[0]
        date_2_yr_before = date_mht_engage - dt.timedelta(360*2)
        df_this_pt = df_EGFR[df_EGFR['RUID']==ruid]
        df_this_pt = df_this_pt.sort('LAB_DATE')
        condition_before_time_window = (df_this_pt['LAB_DATE'] < date_mht_engage) &  (df_this_pt['LAB_DATE']> date_2_yr_before)
        condition_after_time_window = (df_this_pt['LAB_DATE'] > date_mht_engage) 
        
        mean_EGFR_before = np.mean(df_this_pt[condition_before_time_window]['EGFR']) if len(df_this_pt[condition_before_time_window]['EGFR'])>0 else np.nan
        mean_EGFR_after =  np.mean(df_this_pt[condition_after_time_window]['EGFR'] ) if len(df_this_pt[condition_after_time_window]['EGFR'])>0 else np.nan

        #change in EGFR
        change_EGFR = mean_EGFR_after - mean_EGFR_before
        d_change_EGFR[ruid] = change_EGFR
    else: #there are NOT MHT recordings for their BP
        change_EGFR = np.nan
        d_change_EGFR[ruid] = change_EGFR

## join other features to aggreagate        
df_EGFR_aggregate = pd.merge( df_EGFR_aggregate, pd.DataFrame(d_change_EGFR.items(), columns=['RUID', 'change_EGFR']) , how='outer')
