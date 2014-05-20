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
filename = input_folder + 'mht_strategy_20140407.txt'
pd.set_option('display.line_width', 300)
df_MHT_STRATEGY = pd.read_csv(filename, sep='\t')

df_MHT_STRATEGY['STRATEGY_DATE'] = pd.to_datetime(df_MHT_STRATEGY['STRATEGY_DATE'])

df_MHT_STRATEGY['CONTROL_LEVEL'][ df_MHT_STRATEGY['CONTROL_LEVEL'] == 'Out of Control' ] = -1
df_MHT_STRATEGY['CONTROL_LEVEL'][ df_MHT_STRATEGY['CONTROL_LEVEL'] == 'In Control' ] = 1

