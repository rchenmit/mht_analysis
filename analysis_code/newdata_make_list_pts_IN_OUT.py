print("running newdata_make_list_pts_IN_OUT.py")

## prepare data
l_pt_ruid_MHT = list_ruid #grab the list of patient ID's that overlap with MHT

l_pt_ruid_CLINICIAN = []
l_pt_ruid_RECORD_NUMBER = []
l_pt_ruid_CLINICIAN_IN_CONTROL = []
l_pt_ruid_CLINICIAN_OUT_CONTROL = []

for i in l_pt_ruid_MHT:
    if i in d_bp_status_pt_level_clinician: #if clinician determined BP, and if status is not mixed
        l_pt_ruid_CLINICIAN.append(i)
    if i in d_bp_status_pt_level: #if BP record was made, and if status is not mixed
        l_pt_ruid_RECORD_NUMBER.append(i)
    if i in d_bp_status_pt_level_clinician and d_bp_status_pt_level_clinician[i] == 1:
        l_pt_ruid_CLINICIAN_IN_CONTROL.append(i)
    if i in d_bp_status_pt_level_clinician and d_bp_status_pt_level_clinician[i] == -1:
        l_pt_ruid_CLINICIAN_OUT_CONTROL.append(i)
## pick response variable
