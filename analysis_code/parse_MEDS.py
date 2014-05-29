## Robert Chen
## Monday 5/12/2014
##
## read and process BMI file
##
##
import datetime as dt
import pandas as pd

## options
input_folder = '../../data/new_data_20140416/Data_20140409/'
output_dir = '../../data/new_data_20140416/Data_curated_RC/'


## Prepare data, read data
read_filename = input_folder + 'Meds_DD_04082014_withHeader.csv'
store_filename = input_folder + "df_MEDS.h5"

store = pd.HDFStore(store_filename, mode = 'w')
for chunk in pd.read_csv(read_filename, chunksize=500000, escapechar='\\'):
    
    store.append('df_MEDS', chunk)
store.close()


#pd.set_option('display.line_width', 300)
#df_MEDS_part1 = pd.read_csv(filename1, sep=',' , escapechar='\\')
#df_MEDS_part2 = pd.read_csv(filename2, sep=',' , escapechar='\\')
#
#df_MEDS_part1['Entry_Date'] = pd.to_datetime(df_MEDS_part1['Entry_Date'])
#df_MEDS_part2['Entry_Date'] = pd.to_datetime(df_MEDS_part2['Entry_Date'])

