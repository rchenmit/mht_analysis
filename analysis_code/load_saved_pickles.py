## load saved pickles
pickle_dir = '../analysis_output/pickle/'

## import these
#import pickle
if sys.version_info.major == 3:
    import pickle
else:
    import cPickle as pickle


## load pickles
pickle_file = pickle_dir + 'list_ruid.pickle'
with open(pickle_file, 'rb') as fhandle:
    list_ruid = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'df_bp_clinician.pickle'
with open(pickle_file, 'rb') as fhandle:
    df_bp_clinician = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'df_bp_record.pickle'
with open(pickle_file, 'rb') as fhandle:
    df_bp_record = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'df_egfr_record.pickle'
with open(pickle_file, 'rb') as fhandle:
    df_egfr_record = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'd_bp_record.pickle'
with open(pickle_file, 'rb') as fhandle:
    d_bp_record = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'd_bp_status_pt_level.pickle'
with open(pickle_file, 'rb') as fhandle:
    d_bp_status_pt_level = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'd_bp_clinician.pickle'
with open(pickle_file, 'rb') as fhandle:
    d_bp_clinician = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'd_bp_status_pt_level_clinician.pickle'
with open(pickle_file, 'rb') as fhandle:
    d_bp_status_pt_level_clinician = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'd_other_diag_clinician_binary.pickle'
with open(pickle_file, 'rb') as fhandle:
    d_other_diag_clinician_binary = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'd_other_diag_clinician.pickle'
with open(pickle_file, 'rb') as fhandle:
    d_other_diag_clinician = pickle.load(fhandle)
fhandle.close()

pickle_file = pickle_dir + 'd_other_diag_pt_level_clinician.pickle'
with open(pickle_file, 'rb') as fhandle:
    d_other_diag_pt_level_clinician = pickle.load(fhandle)
fhandle.close()

