## preparing example data for VIP class purposes
## use 30 pts with DM, and 30 overall from the entire dataset (there may be some overlap)
import pandas as pd
import cPickle as pickle


#output folder
output_dir = '../../VIP_sample_data/'


## load pickles
pickle_dir = '../analysis_output/pickle/'
pickle_file = pickle_dir + 'df_bp_clinician.pickle'
with open(pickle_file, 'rb') as fhandle:
    df_bp_clinician = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'd_other_diag_clinician.pickle'
with open(pickle_file, 'rb') as fhandle:
    d_other_diag_clinician = pickle.load(fhandle)
fhandle.close()



list1_DM = d_other_diag_clinician['dm'].keys()
list2_HTN = d_bp_clinician.keys()

diff = set(list2_HTN).difference( set(list1_DM)) 
diff = list(diff) #cast the set as a list

ruid_DM = list1_DM[0:15] #15 patients with DM
ruid_NO_DM = diff[0:15] #15 patients that do NOT have DM

all_sample_ruid = ruid_DM + ruid_NO_DM
all_sample_status = [1]*15 + [0]*15

## Prepare data, read data in as chunks
read_filename = input_folder + 'Meds_DD_04082014_withHeader.csv'


df_sample_MEDS = pd.DataFrame()
print "reading chunks, ~11.2M lines total; 500K chunks each"
cnt = 0
for chunk in pd.read_csv(read_filename, chunksize=500000, escapechar='\\'):
    cnt = cnt + 1
    print cnt
    df_meds_in_sample = chunk[chunk['RUID'].isin(all_sample_ruid)]
    df_sample_MEDS = df_sample_MEDS.append(df_meds_in_sample)

#write dataframes to CSV files
df_sample_MEDS.to_csv( output_dir + 'df_sample_MEDS.csv', index = False)



