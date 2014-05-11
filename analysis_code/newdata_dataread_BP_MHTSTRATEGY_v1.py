## Robert Chen
## Monday 3/12/2014
##
## trying to parse this in python
##
import os
import sys
if os.name == 'nt': #'nt' = windows
    sys.path.append('C:\\anaconda\\lib\\site-packages') #in windows, alot of modules were installed with Anaconda
import pandas as pd
import numpy as np
import math
import copy
import csv
import scipy as s
import openpyxl
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from dateutil import parser
from collections import Counter
#import pickle
if sys.version_info.major == 3:
    import pickle
else:
    import cPickle as pickle


## ENTER import files ##########################################################################################################
datadir = '../data/new_data_20140416/Data_20140409/'
filename = datadir + 'Meds_DD_04082014.csv'
file_classes = datadir + 'MedClasses.xlsx'
file_BP_clinician = datadir + 'mht_strategy_20140407.txt'
file_BP_record = datadir + 'BP_04082014.csv'
file_eGFR_record = datadir + 'EGFR_04082014.csv'
###file_labs_record = datadir + 'labs.txt'
l_file_labs_record = [datadir + 'labs_chunkaa.txt', datadir + 'labs_chunkab.txt', datadir + 'labs_chunkac.txt',
                      datadir + 'labs_chunkad.txt', datadir + 'labs_chunkae.txt', datadir + 'labs_chunkaf.txt',
                      datadir + 'labs_chunkag.txt', datadir + 'labs_chunkah.txt', datadir + 'labs_chunkai.txt',
                      datadir + 'labs_chunkaj.txt', datadir + 'labs_chunkak.txt', datadir + 'labs_chunkal.txt',
                      datadir + 'labs_chunkam.txt', datadir + 'labs_chunkan.txt', datadir + 'labs_chunkao.txt',
                      datadir + 'labs_chunkap.txt', datadir + 'labs_chunkaq.txt', datadir + 'labs_chunkar.txt',
                      datadir + 'labs_chunkas.txt', datadir + 'labs_chunkat.txt', datadir + 'labs_chunkau.txt',
                      datadir + 'labs_chunkav.txt', datadir + 'labs_chunkaw.txt', datadir + 'labs_chunkax.txt']
l_file_icd9_codes = [datadir + 'icd9_codes_chunkaa.txt', datadir + 'icd9_codes_chunkab.txt', datadir + 'icd9_codes_chunkac.txt',
                     datadir + 'icd9_codes_chunkad.txt', datadir + 'icd9_codes_chunkae.txt', datadir + 'icd9_codes_chunkaf.txt']

## Functions  ############################################################################################################
def read_csv_to_df(filename, delim):
    reader = csv.reader(open(filename, 'rU'), delimiter=delim)
    l_headers = next(reader)
    print(l_headers)
    num_cols = len(l_headers)
    indexes_for_df = np.array([])
    data = []
    print("reading in the raw data: ---------------------\n")
    cnt = 0
    for row in reader:
        cnt +=1
        if (cnt % 10000 == 0):
            print(str(cnt)+ " lines read")
        index_ruid_raw = row[0]
        if index_ruid_raw != "":
            index_ruid = int(index_ruid_raw)
            indexes_for_df = np.append(indexes_for_df, index_ruid)
            vals_for_row = []
            for i in range(1, num_cols):
                vals_for_row.append(row[i])
            data.append(vals_for_row)
    df_data = pd.DataFrame(data, index = indexes_for_df, columns = l_headers[1:])
    return df_data

    
def read_csv_to_df_med(filename, delim):
    print("start reading in raw data: ----------------\n")
    reader = csv.reader(open(filename, 'rU'), delimiter=delim)
    l_headers = next(reader)
    
    index_ruid = np.array([]) #all the patient RUID's
    index_drug = np.array([])
    data_for_pt = [] #all the associated data; row by row
    data_for_drug = []
    
    print("reading in the raw data: ---------------------- \n")
    cnt = 0
    for row in reader:
        cnt +=1
        if (cnt % 10000 == 0):
            print(str(cnt) +  " lines read so far")
        ruid = int(row[0])
        entry_date = pd.to_datetime(row[1])
        drug_name = row[2]
        drug_form = row[3]
        drug_strength = row[4]
        route = row[5]
        dose_amt = row[6]
        drug_freq = row[7]
        duration = row[8]

        index_ruid = np.append(index_ruid, ruid) #add RUID
        index_drug = np.append(index_drug, drug_name)
        data_for_pt.append([entry_date, drug_name,drug_form,drug_strength,dose_amt,route, drug_freq,duration])
        data_for_drug.append([ruid, entry_date, drug_form,drug_strength,dose_amt,route, drug_freq,duration])
    
    #create pandas dataframe with patient RUID as index
    df_data_pt = pd.DataFrame(data_for_pt, index=index_ruid, columns=l_headers[1:9])
    df_data_drug = pd.DataFrame(data_for_drug, index = index_drug, columns = np.concatenate([l_headers[0:2],l_headers[3:9]]))
    return df_data_pt, df_data_drug

    

## Read in blood pressures; eGFR; labs.txt convert to time series  ################################################################################
df_bp_clinician = read_csv_to_df(file_BP_clinician, '\t')
df_bp_record = read_csv_to_df(file_BP_record, ',')
df_egfr_record = read_csv_to_df(file_eGFR_record, ',')
#df_labs_record = read_csv_to_df(file_labs_record)

#
##read in labs separately
#d_df_labs_record_chunk_readin = dict()
#df_labs_record = pd.DataFrame() #initialize df
#d_df_icd_chunk_readin = dict()
#df_icd_codes = pd.DataFrame()
##for the labs
#for labchunk in l_file_labs_record:
#    d_df_labs_record_chunk_readin[labchunk] = read_csv_to_df(labchunk)
##for the ICD9 codes
#for chunk in l_file_icd9_codes:
#    d_df_icd_chunk_readin[chunk]  = read_csv_to_df(chunk)
#    

#pickle
with open(r"df_bp_clinician.pickle", "wb") as output_file:
    pickle.dump(df_bp_clinician, output_file)
output_file.close()

with open(r"df_bp_record.pickle", "wb") as output_file:
    pickle.dump(df_bp_record, output_file)
output_file.close()

with open(r"df_egfr_record.pickle", "wb") as output_file:
    pickle.dump(df_egfr_record, output_file)
output_file.close()

#
###with open(r"df_labs_record.pickle", "wb") as output_file:
###    pickle.dump(df_labs_record, output_file)
###output_file.close()
###
###with open(r"df_icd_codes.pickle", "wb") as output_file:
###    pickle.dump(df_icd_codes, output_file)
###output_file.close()
#
#p1 = pickle.Pickler(open("d_df_labs_record_chunk_readin.pickle", "wb"))
#p1.fast = True
#p1.dump(d_df_labs_record_chunk_readin)
#
#p2 = pickle.Pickler(open("d_df_icd_chunk_readin.pickle", "wb"))
#p2.fast = True
#p2.dump(d_df_icd_chunk_readin)
#


## analyze recorded BP's: using BP.txt (reported numbers)#################################################################################
#list_ruid = list(set(df_data_by_pt.index.values)) #list of floats
list_ruid = list(set(df_bp_clinician.index.values)) #list of floats
#earliest and latest possible date : for throwing out bad data
early_date = datetime(1990,1,1)
late_date = datetime.today()

#make dictionary of BP's key'd by RUID
d_bp_record = dict()
cnt = 0
print("bulding dictionary of recorded BP's (346K lines total)-----------------\n")
for i in range(len(df_bp_record)):
    cnt+=1
    if (cnt % 10000 == 0):
        print(cnt) 
    key = df_bp_record.index[i]
    indexes_for_df = np.array([])
    data = []
    this_date = parser.parse(df_bp_record.iloc[i]['MEASURE_DATE']) ##PARSE THE DATE OUT!
    bool_this_date_good = this_date > early_date and this_date < late_date
    indexes_for_df = np.append(indexes_for_df, this_date)
    if df_bp_record.iloc[i]['SYSTOLIC'].isdigit() and df_bp_record.iloc[i]['DIASTOLIC'].isdigit() and bool_this_date_good:
        data.append([int(df_bp_record.iloc[i]['SYSTOLIC']), int(df_bp_record.iloc[i]['DIASTOLIC'])]) #CAST ELEMENTS AS INTEGERS!!!!
        if key in d_bp_record: #then append
            d_bp_record[key] = d_bp_record[key].append(pd.DataFrame(data, index = indexes_for_df, columns = ['SYSTOLIC', 'DIASTOLIC']))
        else: #then initialize
            d_bp_record[key] = pd.DataFrame(data, index = indexes_for_df, columns = ['SYSTOLIC', 'DIASTOLIC'])

#add in status at each time point
print("calculating BP control status from recorded numbers: \n")
for key in d_bp_record: #loop thru the keys in dictionary
    d_bp_record[key]['STATUS'] = 0
    bool_condition_systolic = d_bp_record[key]['SYSTOLIC'] < 140
    bool_condition_diastolic = d_bp_record[key]['DIASTOLIC'] < 90
    bool_condition_INCONTROL = bool_condition_systolic & bool_condition_diastolic
    d_bp_record[key].loc[bool_condition_INCONTROL, 'STATUS'] = 1 #-1 => IN CONTROL
    d_bp_record[key].loc[~bool_condition_INCONTROL, 'STATUS'] = -1 #1 => OUT OF CONTROL
            
#make dictionary of BP Control Status (at the patient level, ie mostly in control or out of control)
print("calculating intervals of in control vs out of control from recorded numbers: \n")
d_bp_status_pt_level = dict()
for key in d_bp_record:
    d_days_in_out = {-1: 0, 1:0}
    ts_status_this_pt = d_bp_record[key]['STATUS'].sort_index()
    last_status = ts_status_this_pt[0]
    last_timestamp = ts_status_this_pt.index[0]

    if len(ts_status_this_pt) > 1 and (max(ts_status_this_pt.index) - min(ts_status_this_pt.index)).days > 1: #if there are more than 1 entry, and more than 1 day's worth (if theres more than one entry and they're not all on the same day)
        #loop thru the timeSeries of status for this patient
        for timestamp in ts_status_this_pt.index:
            time_delta = (timestamp - last_timestamp).days
            d_days_in_out[last_status] += time_delta #add the time that has passed
            if ts_status_this_pt[timestamp].size > 1:
                status_at_this_timestamp = ts_status_this_pt[timestamp][-1] #pick the last recorded status for this timestamp
                if status_at_this_timestamp != last_status: #if the status changed
                    last_status = status_at_this_timestamp           
            else:
                status_at_this_timestamp = ts_status_this_pt[timestamp]
                if status_at_this_timestamp != last_status: #if the status changed
                    last_status = status_at_this_timestamp #then change last_status to reflect this so that you add to the right status for the next timestamp
            last_timestamp = timestamp
                
        #now count how many days in /out and detemrine if mostly in or mostly out or mixed
        num_in = d_days_in_out[1]
        num_out = d_days_in_out[-1]
    else: #if only one BP measurement was taken for the patient
        if last_status == 1:
            num_in = 1
            num_out = 0
        else:
            num_in = 0
            num_out = 1  
    
    if num_in == 0 and num_out == 0:
        print("ERROR 0: no days in or out!  " + str(key))
        d_bp_status_pt_level[key] = 0
    elif num_out == 0:
        if num_in > num_out:
            d_bp_status_pt_level[key] = 1
        else:
            print("ERROR1 - check!")
    elif num_in == 0:
        if num_out > num_in:
            d_bp_status_pt_level[key] = -1
        else:
            print("ERROR2 - check!")
    elif num_in > num_out and num_out == 0:
        d_bp_status_pt_level[key] = 1
    elif num_out > num_in and num_in == 0:
        d_bp_status_pt_level[key] = -1
    elif num_in / float(num_out) > 1.5:
        d_bp_status_pt_level[key] = 1
    elif num_out / float(num_in) > 1.5:
        d_bp_status_pt_level[key] = -1
    else:
        d_bp_status_pt_level[key] = 0
        
#print counts
print("number patients with each control class (from numbers: ")
counter_control_status = Counter(val for val in d_bp_status_pt_level.values())
print(counter_control_status)

#pickle:
with open(r"d_bp_record.pickle", "wb") as output_file:
    pickle.dump(d_bp_record, output_file)
output_file.close()

with open(r"d_bp_status_pt_level.pickle", "wb") as output_file:
    pickle.dump(d_bp_status_pt_level, output_file)
output_file.close()

