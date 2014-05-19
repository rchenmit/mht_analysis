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
filename = input_folder + 'CPT_04082014.csv'
pd.set_option('display.line_width', 300)
df_CPT = pd.read_csv(filename, sep=',')

df_CPT['EVENT_DATE'] = pd.to_datetime(df_CPT['EVENT_DATE'])
