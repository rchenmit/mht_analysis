## for debug purpose

key = 99971945
###def debug_status_pt_level_function(key): 
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
            #now count the number of days in the status                                                                                                                                                                                                                                                                                   
        if status_at_this_timestamp != last_status[-1]:
            if last_status[-2]==last_status[-1]: #if the status changed and there were two consecutive recordings of the same last status                                                                                                                                                                                             
                d_days_in_out[last_status[1]] += time_delta
                last_status[0] = last_status[1]
                last_status[1] = status_at_this_timestamp
            elif last_status[0]==fakestatus:
                last_status[0] = last_status[1]
                last_status[1] = status_at_this_timestamp
            else:
                d_days_in_out[last_status[0]] += time_delta
                last_status[0] = last_status[0] #since there was only one instance of the new instance (doesn't have 2 consecutive) then we'll treat last_status[0] as the same as the status before it                                                                                                                               
                last_status[1] = status_at_this_timestamp
        elif last_status[0] != fakestatus:
            d_days_in_out[last_status[1]] += time_delta
            last_status[0] = last_status[1]
            last_status[1] = status_at_this_timestamp
        else:#base case, where last_status[0] is fake status                                                                                                                                                                                                                                                                          
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
    d_bp_status_pt_level_clinician_this_key = 0
elif num_out == 0:
    if num_in > num_out:
        d_bp_status_pt_level_clinician_this_key = 1
    else:
        print("ERROR1 - check!")
elif num_in == 0:
    if num_out > num_in:
        d_bp_status_pt_level_clinician_this_key = -1
    else:
        print("ERROR2 - check!")
elif num_in > num_out and num_out == 0:
    d_bp_status_pt_level_clinician_this_key = 1
elif num_out > num_in and num_in == 0:
    d_bp_status_pt_level_clinician_this_key = -1
elif num_in / float(num_out) > 1.5:
    d_bp_status_pt_level_clinician_this_key = 1
elif num_out / float(num_in) > 1.5:
    d_bp_status_pt_level_clinician_this_key = -1
else:
    d_bp_status_pt_level_clinician_this_key = 0
