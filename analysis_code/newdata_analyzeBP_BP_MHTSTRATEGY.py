## analyze recorded BP's
## note: run this AFTER you have run newdata_dataread_BP_MHTSTRATEGY_v1.py
##
##################################################################################
from __future__ import print_function
output_file = './newdata_analyzeBP_BP_MHTSTRATEGY.may6.out'
fstream = open(output_file, 'a')

print("running newdata_analyzeBP_BP_MHTSTRATEGY.py")
## analyze recorded BP status: using MHT_strategy.txt (physician reported)######################################################################################
d_bp_clinician = dict()
d_other_diag_clinician_binary = dict()
d_other_diag_clinician = dict()
cnt = 0
print("bulding dictionary of clinician determined BP statuses (37K lines total in input file 'mht_strategy_20140407.txt')-----------------\n")
#note: not all lines are htn, some lines are for Diabetes (dm) control status!
for i in range(len(df_bp_clinician)):
    cnt+=1
    if (cnt % 10000 == 0):
        print(cnt) 
    key = df_bp_clinician.index[i]
    indexes_for_df = np.array([])
    data = [] #this only has data for THIS LINE!
    this_date = parser.parse(df_bp_clinician.iloc[i]['STRATEGY_DATE']) ##PARSE THE DATE OUT!
    this_disease = df_bp_clinician.iloc[i]['DISEASE']
    if this_disease == "htn": ##only analyze the lines in dataframe where the disease is HTN!!
        indexes_for_df = np.append(indexes_for_df, this_date)
        if df_bp_clinician.iloc[i]['CONTROL_LEVEL'] == 'In Control':
            data.append(1) #1 = in control
            if key in d_bp_clinician: #then append
                d_bp_clinician[key] = d_bp_clinician[key].append(pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS']))
            else: #then initialize
                d_bp_clinician[key] = pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS'])
        elif df_bp_clinician.iloc[i]['CONTROL_LEVEL'] == 'Out of Control':
            data.append(-1) #-1 = out of control
            if key in d_bp_clinician: #then append
                d_bp_clinician[key] = d_bp_clinician[key].append(pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS']))
            else: #then initialize
                d_bp_clinician[key] = pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS'])
    else: #if its another disease, mark the existence of the other disease
        if this_disease in d_other_diag_clinician:
            d_other_diag_clinician_binary[this_disease][key] = 1
            indexes_for_df = np.append(indexes_for_df, this_date)
            if df_bp_clinician.iloc[i]['CONTROL_LEVEL'] == 'In Control': #this checks for 'In Control' regarding the other disease (DM or CHF), NOT hypertension!
                data.append(1) #1 = in control
                if key in d_other_diag_clinician[this_disease]: #then append
                    d_other_diag_clinician[this_disease][key] = d_other_diag_clinician[this_disease][key].append(pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS']))
                else: #then initialize
                    d_other_diag_clinician[this_disease][key] = pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS'])
            elif df_bp_clinician.iloc[i]['CONTROL_LEVEL'] == 'Out of Control':
                data.append(-1) #-1 = out of control
                if key in d_other_diag_clinician[this_disease]: #then append
                    d_other_diag_clinician[this_disease][key] = d_other_diag_clinician[this_disease][key].append(pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS']))
                else: #then initialize
                    d_other_diag_clinician[this_disease][key] = pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS'])    
        else:
            d_other_diag_clinician_binary[this_disease] = dict()
            d_other_diag_clinician_binary[this_disease][key] = 1
            d_other_diag_clinician[this_disease] = dict()
            indexes_for_df = np.append(indexes_for_df, this_date)
            if df_bp_clinician.iloc[i]['CONTROL_LEVEL'] == 'In Control':
                data.append(1) #1 = in control
                if key in d_other_diag_clinician[this_disease]: #then append
                    d_other_diag_clinician[this_disease][key] = d_other_diag_clinician[this_disease][key].append(pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS']))
                else: #then initialize
                    d_other_diag_clinician[this_disease][key] = pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS'])
            elif df_bp_clinician.iloc[i]['CONTROL_LEVEL'] == 'Out of Control':
                data.append(-1) #-1 = out of control
                if key in d_other_diag_clinician[this_disease]: #then append
                    d_other_diag_clinician[this_disease][key] = d_other_diag_clinician[this_disease][key].append(pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS']))
                else: #then initialize
                    d_other_diag_clinician[this_disease][key] = pd.DataFrame(data, index = indexes_for_df, columns = ['STATUS'])    
     
    
        
#make dictionary of BP Control Status (at the patient level, ie mostly in control or out of control)
print("calculating intervals of in control vs out of control from recorded numbers: \n")
d_bp_status_pt_level_clinician = dict()
for key in d_bp_clinician:
    d_days_in_out = {-1: 0, 1:0}
    ts_status_this_pt = d_bp_clinician[key]['STATUS'].sort_index()
    fakestatus = -999
    last_status = [fakestatus, ts_status_this_pt[0]] #initialize it to some arbitrary value (-999) and the FIRST value in the timeseries for this patient
    last_timestamp = ts_status_this_pt.index[0]

    if len(ts_status_this_pt) > 1 and (max(ts_status_this_pt.index) - min(ts_status_this_pt.index)).days > 1: #if there are more than 1 entry, and more than 1 day's worth (if theres more than one entry and they're not all on the same day)
        #loop thru the timeSeries of status for this patient
        for timestamp in ts_status_this_pt.index:
            time_delta = (timestamp - last_timestamp).days
            if not np.isscalar(ts_status_this_pt[timestamp]): #if multiple status for this timestamp
                status_at_this_timestamp = ts_status_this_pt[timestamp][-1]#pick the last recorded status for this timestamp
            else:
                status_at_this_timestamp = ts_status_this_pt[timestamp] #pick the status (its only one scalar)
                if status_at_this_timestamp != last_status[-1]:
                    if last_status[-2]==last_status[-1]: #if the status changed and there were two consecutive recordings of the same last status
                        d_days_in_out[last_status[1]] += time_delta
                        last_status[0] = last_status[1]
                        last_status[1] = status_at_this_timestamp
                    else:
                        d_days_in_out[last_status[0]] += time_delta
                        last_status[0] = last_status[0] #since there was only one instance of the new instance (doesn't have 2 consecutive) then we'll treat last_status[0] as the same as the status before it
                        last_status[1] = status_at_this_timestamp
                elif last_status[0] != fakestatus:
                    d_days_in_out[last_status[0]] += time_delta
                    last_status[0] = last_status[1]
                    last_status[1] = status_at_this_timestamp
                else:
                    d_days_in_out[last_status[1]] += time_delta
                    last_status[0] = last_status[1]
                    last_status[1] = status_at_this_timestamp
            last_timestamp = timestamp
        #now count how many days in /out and detemrine if mostly in or mostly out or mixed
        num_in = d_days_in_out[1]
        num_out = d_days_in_out[-1]
    else: #if only one BP measurement was taken for the patient
        if last_status[-1] == 1:
            num_in = 1
            num_out = 0
        else:
            num_in = 0
            num_out = 1  
    
    if num_in == 0 and num_out == 0:
        print("ERROR 0: no days in or out!  " + str(key))
        d_bp_status_pt_level_clinician[key] = 0
    elif num_out == 0:
        if num_in > num_out:
            d_bp_status_pt_level_clinician[key] = 1
        else:
            print("ERROR1 - check!")
    elif num_in == 0:
        if num_out > num_in:
            d_bp_status_pt_level_clinician[key] = -1
        else:
            print("ERROR2 - check!")
    elif num_in > num_out and num_out == 0:
        d_bp_status_pt_level_clinician[key] = 1
    elif num_out > num_in and num_in == 0:
        d_bp_status_pt_level_clinician[key] = -1
    elif num_in / float(num_out) > 1.5:
        d_bp_status_pt_level_clinician[key] = 1
    elif num_out / float(num_in) > 1.5:
        d_bp_status_pt_level_clinician[key] = -1
    else:
        d_bp_status_pt_level_clinician[key] = 0


#for other diseases, determine at the patient level if in control or out of control
print("calculating intervals of in control vs out of control from recorded numbers [OTHER DIAGNOSIS]: \n")
d_other_diag_pt_level_clinician = dict()
for disease in d_other_diag_clinician:
    d_other_diag_pt_level_clinician[disease] = dict()
    for key in d_other_diag_clinician[disease]:
        if key in d_bp_clinician: #if the BP numbers have been recorded for the patient
            d_days_in_out = {-1: 0, 1:0}
            ts_status_this_pt = d_bp_clinician[key]['STATUS'].sort_index()
            fakestatus = -999
            last_status = [fakestatus, ts_status_this_pt[0]] #initialize it to some arbitrary value (-999) and the FIRST value in the timeseries for this patient
            last_timestamp = ts_status_this_pt.index[0]

            if len(ts_status_this_pt) > 1 and (max(ts_status_this_pt.index) - min(ts_status_this_pt.index)).days > 1: #if there are more than 1 entry, and more than 1 day's worth (if theres more than one entry and they're not all on the same day)
                #loop thru the timeSeries of status for this patient
                for timestamp in ts_status_this_pt.index:
                    time_delta = (timestamp - last_timestamp).days
                    if not np.isscalar(ts_status_this_pt[timestamp]): #if multiple status for this timestamp
                        status_at_this_timestamp = ts_status_this_pt[timestamp][-1]#pick the last recorded status for this timestamp
                    else:
                        status_at_this_timestamp = ts_status_this_pt[timestamp] #pick the status (its only one scalar)
                        if status_at_this_timestamp != last_status[-1]:
                            if last_status[-2]==last_status[-1]: #if the status changed and there were two consecutive recordings of the same last status
                                d_days_in_out[last_status[1]] += time_delta
                                last_status[0] = last_status[1]
                                last_status[1] = status_at_this_timestamp
                            else:
                                d_days_in_out[last_status[0]] += time_delta
                                last_status[0] = last_status[0] #since there was only one instance of the new instance (doesn't have 2 consecutive) then we'll treat last_status[0] as the same as the status before it
                                last_status[1] = status_at_this_timestamp
                        elif last_status[0] != fakestatus:
                            d_days_in_out[last_status[0]] += time_delta
                            last_status[0] = last_status[1]
                            last_status[1] = status_at_this_timestamp
                        else:
                            d_days_in_out[last_status[1]] += time_delta
                            last_status[0] = last_status[1]
                            last_status[1] = status_at_this_timestamp
                    last_timestamp = timestamp
                #now count how many days in /out and detemrine if mostly in or mostly out or mixed
                num_in = d_days_in_out[1]
                num_out = d_days_in_out[-1]
            else: #if only one BP measurement was taken for the patient
                if last_status[-1] == 1:
                    num_in = 1
                    num_out = 0
                else:
                    num_in = 0
                    num_out = 1  
        
            if num_in == 0 and num_out == 0:
                print("ERROR 0: no days in or out!  " + str(key))
                d_other_diag_pt_level_clinician[disease][key] = 0
            elif num_out == 0:
                if num_in > num_out:
                    d_other_diag_pt_level_clinician[disease][key] = 1
                else:
                    print("ERROR1 - check!")
            elif num_in == 0:
                if num_out > num_in:
                    d_other_diag_pt_level_clinician[disease][key] = -1
                else:
                    print("ERROR2 - check!")
            elif num_in > num_out and num_out == 0:
                d_other_diag_pt_level_clinician[disease][key] = 1
            elif num_out > num_in and num_in == 0:
                d_other_diag_pt_level_clinician[disease][key] = -1
            elif num_in / float(num_out) > 1.5:
                d_other_diag_pt_level_clinician[disease][key] = 1
            elif num_out / float(num_in) > 1.5:
                d_other_diag_pt_level_clinician[disease][key] = -1
            else:
                d_other_diag_pt_level_clinician[disease][key] = 0

        
#print counts
print("number patients with each control class (from clinician assessment): ", file=fstream)
counter_control_status = Counter(val for val in d_bp_status_pt_level_clinician.values())
print(counter_control_status, file = fstream)
#print counts for OTHER diagnosis
print("number patients with each control status for OTHER disease (from clinician assessment): ", file=fstream)
for dz in d_other_diag_pt_level_clinician:
    print(dz, file=fstream)
    counter_control_status = Counter(val for val in d_other_diag_pt_level_clinician[dz].values())
    print(counter_control_status, file=fstream)

fstream.close()
#pickle
with open(r"d_bp_clinician.pickle", "wb") as output_file:
    pickle.dump(d_bp_clinician, output_file)
output_file.close()

with open(r"d_bp_status_pt_level_clinician.pickle", "wb") as output_file:
    pickle.dump(d_bp_status_pt_level_clinician, output_file)
output_file.close()

with open(r"d_other_diag_clinician_binary.pickle", "wb") as output_file:
    pickle.dump(d_other_diag_clinician_binary, output_file)
output_file.close()

with open(r"d_other_diag_clinician.pickle", "wb") as output_file:
    pickle.dump(d_other_diag_clinician, output_file)
output_file.close()

with open(r"d_other_diag_pt_level_clinician.pickle", "wb") as output_file:
    pickle.dump(d_other_diag_pt_level_clinician, output_file)
output_file.close()
