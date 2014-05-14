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
filename = input_folder + 'BMI_04082014.csv'
pd.set_option('display.line_width', 300)
df_BMI = pd.read_csv(filename)
df_BMI['Weight_Date'] = pd.to_datetime(df_BMI['Weight_Date'])

## make dictionary of average values for these features:
##  Weight, Height, BMI, Change in BMI before/after MHT, pregnant

columns_for_df = df_BMI.columns
df_BMI_aggregate = df_BMI.groupby(df_BMI.RUID).mean()


## calculate other features (that can't be averaged bc they're not numbers): change in BMI, pregnancy before/after
d_change_BMI = dict()
d_pregnant_before = dict()
d_pregnant_after = dict()

for ruid in df_BMI_aggregate.index:
    if ruid in d_bp_clinician: #there are MHT recordings for their BP
        date_mht_first_record = min(d_bp_clinician[ruid].index).date()
        date_2_yr_before = date_mht_first_record - dt.timedelta(360*2)
        df_this_pt = df_BMI[df_BMI['RUID']==ruid]
        df_this_pt = df_this_pt.sort('Weight_Date')
        condition_before_time_window = (df_this_pt['Weight_Date'] < date_mht_first_record) &  (df_this_pt['Weight_Date']> date_2_yr_before)
        condition_after_time_window = (df_this_pt['Weight_Date'] > date_mht_first_record) 
        
        mean_BMI_before = np.mean(df_this_pt[condition_before_time_window]['BMI']) if len(df_this_pt[condition_before_time_window]['BMI'])>0 else np.nan
        mean_BMI_after =  np.mean(df_this_pt[condition_after_time_window]['BMI'] ) if len(df_this_pt[condition_after_time_window]['BMI'])>0 else np.nan
        pregnant_before_max = max(df_this_pt[condition_before_time_window]['Pregnancy_Indicator']) if len(df_this_pt[condition_before_time_window]['Pregnancy_Indicator']) > 0 else np.nan
        pregnant_after_max  = max(df_this_pt[condition_after_time_window]['Pregnancy_Indicator']) if len(df_this_pt[condition_after_time_window]['Pregnancy_Indicator']) > 0 else np.nan
        if pregnant_before_max == 'Y':
            pregnant_before_ind = 1
        else:
            pregnant_before_ind = 0
        if pregnant_after_max == 'Y':
            pregnant_after_ind = 1
        else:
            pregnant_after_ind = 0
        #change in BMI
        change_BMI = mean_BMI_after - mean_BMI_before
        d_change_BMI[ruid] = change_BMI
        d_pregnant_before[ruid] = pregnant_before_ind
        d_pregnant_after[ruid] = pregnant_after_ind
    else: #there are NOT MHT recordings for their BP
        pregnant_before_ind = np.nan
        pregnant_after_ind = np.nan
        change_BMI = np.nan
        d_change_BMI[ruid] = change_BMI
        d_pregnant_before[ruid] = pregnant_before_ind
        d_pregnant_after[ruid] = pregnant_after_ind

## join other features to aggreagate        
df_BMI_aggregate = pd.merge( df_BMI_aggregate, pd.DataFrame(d_change_BMI.items(), columns=['RUID', 'change_BMI']) , how='outer')
df_BMI_aggregate = pd.merge( df_BMI_aggregate, pd.DataFrame(d_pregnant_before.items(), columns=['RUID', 'pregnant_before']), how='outer')
df_BMI_aggregate = pd.merge( df_BMI_aggregate, pd.DataFrame(d_pregnant_after.items(), columns=['RUID', 'pregnant_after']),  how='outer')

