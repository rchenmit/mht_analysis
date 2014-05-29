## Robert Chen
## Monday 5/12/2014
##
## read and process BMI file
##
##
import datetime as dt

## options
input_folder = '../../data/new_data_20140416/Data_20140409/chunk_data/'
output_dir = '../../data/new_data_20140416/Data_curated_RC/'


## Prepare data, read data
filename1 = input_folder + 'Meds_DD_04082014_part1_withHeader.csv'
filename2 = input_folder + 'Meds_DD_04082014_part2_withHeader.csv'

pd.set_option('display.line_width', 300)
df_MEDS_part1 = pd.read_csv(filename1, sep=',' , escapechar='\\')
df_MEDS_part2 = pd.read_csv(filename2, sep=',' , escapechar='\\')

df_MEDS_part1['Entry_Date'] = pd.to_datetime(df_MEDS_part1['Entry_Date'])
df_MEDS_part2['Entry_Date'] = pd.to_datetime(df_MEDS_part2['Entry_Date'])

