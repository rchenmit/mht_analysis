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
filename = input_folder + 'BP_04082014.csv'
pd.set_option('display.line_width', 300)
df_BP = pd.read_csv(filename, sep=',')

df_BP['MEASURE_DATE'] = pd.to_datetime(df_BP['MEASURE_DATE'])
df_BP['MAP'] = df_BP['SYSTOLIC']*1/3 + df_BP['DIASTOLIC']*2/3
