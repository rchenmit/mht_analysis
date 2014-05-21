## Do a KS test for BP differences before vs. after MHT
## Plot MEDIAN BP before /after MHT
##
##############################################

from __future__ import print_function
from scipy.stats import ks_2samp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as datetime

print("running ./KS_2samp_test_before_after_MHT_stratComorbid.py")
output_dir = '../analysis_output/'
output_file = output_dir + 'KS_2samp_test_before_after_MHT_stratComorbid.out'
fstream = open(output_file,'a')

## calculate before/after MAP's for all pts in MHT
data_BP_stratComorbid = dict()
for dz in d_other_diag_pt_level_clinician:
    data_BP_stratComorbid[dz] = dict()

for dz in data_BP_stratComorbid:
    d_bp_before_after_MHT_thisComorbid = dict()
    d_bp_before_after_MHT_thisComorbid['BEFORE'] = dict()
    d_bp_before_after_MHT_thisComorbid['AFTER'] = dict()
    d_kstest_before_after_MHT = dict()
    d_kstest_before_after_MHT['MAP'] = dict()
    d_kstest_before_after_MHT['SYSTOLIC'] = dict()
    d_kstest_before_after_MHT['DIASTOLIC'] = dict()
    d_list_pressures_before_after = dict()
    d_list_pressures_before_after['BEFORE'] = dict()
    d_list_pressures_before_after['AFTER'] = dict()
    for key in d_other_diag_pt_level_clinician[dz]:
        if key in d_bp_record and key in d_bp_clinician:
            df_bp_this_pt = d_bp_record[key]
            df_bp_this_pt['MAP'] = 1/float(3)*df_bp_this_pt['SYSTOLIC'] + 2/float(3)*df_bp_this_pt['DIASTOLIC']
            df_bp_this_pt = df_bp_this_pt.sort_index()
            date_mht_first_record = min(d_bp_clinician[key].index).date()
            date_mht_engage_date = df_Phenotype[df_Phenotype['RUID'] == key]['ENGAGE_DATE'].values[0].date()
            date_1_yr_before = date_mht_engage_date - datetime.timedelta(360*1)
            date_2_yr_before = date_mht_engage_date - datetime.timedelta(360*2)
            date_3_yr_before = date_mht_engage_date - datetime.timedelta(360*3)

            condition_before_time_window = (df_bp_this_pt.index.date < date_mht_engage_date) & (df_bp_this_pt.index.date > date_2_yr_before)

            
            median_systolic_before = np.median(df_bp_this_pt.loc[condition_before_time_window]['SYSTOLIC'])
            median_diastolic_before = np.median(df_bp_this_pt.loc[condition_before_time_window]['DIASTOLIC'])
            median_MAP_before = np.median(df_bp_this_pt.loc[condition_before_time_window]['MAP'])
            median_systolic_after = np.median(df_bp_this_pt.loc[df_bp_this_pt.index.date > date_mht_engage_date]['SYSTOLIC'])
            median_diastolic_after = np.median(df_bp_this_pt.loc[df_bp_this_pt.index.date > date_mht_engage_date]['DIASTOLIC'])
            median_MAP_after = np.median(df_bp_this_pt.loc[df_bp_this_pt.index.date > date_mht_engage_date]['MAP'])#

            l_this_pt_MAP_before = list(df_bp_this_pt.loc[condition_before_time_window]['MAP'])
            l_this_pt_MAP_after =  list(df_bp_this_pt.loc[df_bp_this_pt.index.date > date_mht_engage_date]['MAP'])
            l_this_pt_SYSTOLIC_before = list(df_bp_this_pt.loc[condition_before_time_window]['SYSTOLIC'])
            l_this_pt_SYSTOLIC_after =  list(df_bp_this_pt.loc[df_bp_this_pt.index.date > date_mht_engage_date]['SYSTOLIC'])
            l_this_pt_DIASTOLIC_before = list(df_bp_this_pt.loc[condition_before_time_window]['DIASTOLIC'])
            l_this_pt_DIASTOLIC_after =  list(df_bp_this_pt.loc[df_bp_this_pt.index.date > date_mht_engage_date]['DIASTOLIC'])#
    
            d_bp_before_after_MHT_thisComorbid['BEFORE'][key] = dict()
            d_bp_before_after_MHT_thisComorbid['AFTER'][key] = dict()
            d_bp_before_after_MHT_thisComorbid['BEFORE'][key]['SYSTOLIC'] = median_systolic_before
            d_bp_before_after_MHT_thisComorbid['BEFORE'][key]['DIASTOLIC'] = median_diastolic_before
            d_bp_before_after_MHT_thisComorbid['BEFORE'][key]['MAP'] = median_MAP_before
            d_bp_before_after_MHT_thisComorbid['AFTER'][key]['SYSTOLIC'] = median_systolic_after
            d_bp_before_after_MHT_thisComorbid['AFTER'][key]['DIASTOLIC'] = median_diastolic_after
            d_bp_before_after_MHT_thisComorbid['AFTER'][key]['MAP'] = median_MAP_after

            d_bp_before_after_MHT_thisComorbid['AFTER'][key]['MAP_list'] = l_this_pt_MAP_after
            d_bp_before_after_MHT_thisComorbid['AFTER'][key]['SYSTOLIC_list'] = l_this_pt_SYSTOLIC_after
            d_bp_before_after_MHT_thisComorbid['AFTER'][key]['DIASTOLIC_list'] = l_this_pt_DIASTOLIC_after
            d_bp_before_after_MHT_thisComorbid['BEFORE'][key]['MAP_list'] = l_this_pt_MAP_before
            d_bp_before_after_MHT_thisComorbid['BEFORE'][key]['SYSTOLIC_list'] = l_this_pt_SYSTOLIC_before
            d_bp_before_after_MHT_thisComorbid['BEFORE'][key]['DIASTOLIC_list'] = l_this_pt_DIASTOLIC_before

    data_BP_stratComorbid[dz]['d_bp_before_after_MHT'] =  d_bp_before_after_MHT_thisComorbid
###### make lists of before/after MAP's
    l_MAP_before_IC = []
    l_MAP_after_IC = []
    l_SYSTOLIC_before_IC = []
    l_SYSTOLIC_after_IC = []
    l_DIASTOLIC_before_IC = []
    l_DIASTOLIC_after_IC = []
    l_status_for_MAP_comparison_IC = []
    l_MAP_before_OOC = []
    l_MAP_after_OOC = []
    l_SYSTOLIC_before_OOC = []
    l_SYSTOLIC_after_OOC = []
    l_DIASTOLIC_before_OOC = []
    l_DIASTOLIC_after_OOC = []
    l_status_for_MAP_comparison_OOC = []
    ks_MAP_IC = np.array([])
    ks_MAP_OOC = np.array([])
    ks_SBP_IC = np.array([])
    ks_SBP_OOC = np.array([])
    ks_DBP_IC = np.array([])
    ks_DBP_OOC = np.array([])
#######    
    d_this_dz_IN = dict((k, v) for k, v in d_other_diag_pt_level_clinician[dz].items() if v == 1)  #d_other_diag_pt_level_clinician was populated in the script *newdata_analyzeBP_BP_MHTSTRATEGY.py*
    d_this_dz_OUT = dict((k, v) for k, v in d_other_diag_pt_level_clinician[dz].items() if v == -1)
    l_pt_ruid_CLINICIAN_IN_CONTROL = d_this_dz_IN.keys()
    l_pt_ruid_CLINICIAN_OUT_CONTROL = d_this_dz_OUT.keys()
    for ruid in l_pt_ruid_CLINICIAN_IN_CONTROL:
        #make sure that every patient analyzed has MAP and SBP and DBP all recorded!
        if (ruid in d_bp_before_after_MHT_thisComorbid['BEFORE'] and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['MAP']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['MAP']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['SYSTOLIC']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['SYSTOLIC']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['DIASTOLIC']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['DIASTOLIC'])  ):
            l_MAP_before_IC.append(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['MAP'])
            l_MAP_after_IC.append(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['MAP'])
            l_SYSTOLIC_before_IC.append(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['SYSTOLIC'])
            l_SYSTOLIC_after_IC.append(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['SYSTOLIC'])
            l_DIASTOLIC_before_IC.append(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['DIASTOLIC'])
            l_DIASTOLIC_after_IC.append(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['DIASTOLIC'])
            l_status_for_MAP_comparison_IC.append(1)
            l_MAP_before_this_pt = d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['MAP_list'];
            l_MAP_after_this_pt = d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['MAP_list']
            l_SBP_before_this_pt = d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['SYSTOLIC_list'];
            l_SBP_after_this_pt = d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['SYSTOLIC_list']
            l_DBP_before_this_pt = d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['DIASTOLIC_list'];
            l_DBP_after_this_pt = d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['DIASTOLIC_list']
            ks_MAP_IC = np.append(ks_MAP_IC, ks_2samp(l_MAP_before_this_pt, l_MAP_after_this_pt))
            ks_SBP_IC = np.append(ks_SBP_IC, ks_2samp(l_SBP_before_this_pt, l_SBP_after_this_pt))
            ks_DBP_IC = np.append(ks_DBP_IC, ks_2samp(l_DBP_before_this_pt, l_DBP_after_this_pt))

    for ruid in l_pt_ruid_CLINICIAN_OUT_CONTROL:
        if(ruid in d_bp_before_after_MHT_thisComorbid['BEFORE'] and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['MAP']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['MAP']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['SYSTOLIC']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['SYSTOLIC']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['DIASTOLIC']) and
            not np.isnan(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['DIASTOLIC']) ):
            l_MAP_before_OOC.append(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['MAP'])
            l_MAP_after_OOC.append(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['MAP'])
            l_SYSTOLIC_before_OOC.append(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['SYSTOLIC'])
            l_SYSTOLIC_after_OOC.append(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['SYSTOLIC'])
            l_DIASTOLIC_before_OOC.append(d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['DIASTOLIC'])
            l_DIASTOLIC_after_OOC.append(d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['DIASTOLIC'])
            l_status_for_MAP_comparison_OOC.append(-1)
            l_MAP_before_this_pt = d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['MAP_list'];
            l_MAP_after_this_pt = d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['MAP_list']
            l_SBP_before_this_pt = d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['SYSTOLIC_list'];
            l_SBP_after_this_pt = d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['SYSTOLIC_list']
            l_DBP_before_this_pt = d_bp_before_after_MHT_thisComorbid['BEFORE'][ruid]['DIASTOLIC_list'];
            l_DBP_after_this_pt = d_bp_before_after_MHT_thisComorbid['AFTER'][ruid]['DIASTOLIC_list']
            ks_MAP_OOC = np.append(ks_MAP_OOC, ks_2samp(l_MAP_before_this_pt, l_MAP_after_this_pt))
            ks_SBP_OOC = np.append(ks_SBP_OOC, ks_2samp(l_SBP_before_this_pt, l_SBP_after_this_pt))
            ks_DBP_OOC = np.append(ks_DBP_OOC, ks_2samp(l_DBP_before_this_pt, l_DBP_after_this_pt))
            
    ######
    ks_MAP_IC = ks_MAP_IC.reshape(len(ks_MAP_IC)/2, 2)
    ks_MAP_OOC = ks_MAP_OOC.reshape(len(ks_MAP_OOC)/2, 2)
    ks_SBP_IC = ks_SBP_IC.reshape(len(ks_SBP_IC)/2, 2)
    ks_SBP_OOC = ks_SBP_OOC.reshape(len(ks_SBP_OOC)/2, 2)
    ks_DBP_IC = ks_DBP_IC.reshape(len(ks_DBP_IC)/2, 2)
    ks_DBP_OOC = ks_DBP_OOC.reshape(len(ks_DBP_OOC)/2, 2)
    
    ks_MAP_IC_ksStat = ks_MAP_IC[:,0]
    ks_MAP_IC_pval = ks_MAP_IC[:,1]
    ks_MAP_OOC_ksStat = ks_MAP_OOC[:,0]
    ks_MAP_OOC_pval = ks_MAP_OOC[:,1]
    ks_SBP_IC_ksStat = ks_SBP_IC[:,0]
    ks_SBP_IC_pval = ks_SBP_IC[:,1]
    ks_SBP_OOC_ksStat = ks_SBP_OOC[:,0]
    ks_SBP_OOC_pval = ks_SBP_OOC[:,1]
    ks_DBP_IC_ksStat = ks_DBP_IC[:,0]
    ks_DBP_IC_pval = ks_DBP_IC[:,1]
    ks_DBP_OOC_ksStat = ks_DBP_OOC[:,0]
    ks_DBP_OOC_pval = ks_DBP_OOC[:,1]
    
    ks_MAP_IC_minsLogP = [-math.log(x) for x in ks_MAP_IC_pval]
    ks_MAP_OOC_minsLogP = [-math.log(x) for x in ks_MAP_OOC_pval]

    
    ### number of higher/lower after:
    higher_MAP_IC = sum([(after-before)>=0 for (after, before) in zip(l_MAP_after_IC, l_MAP_before_IC)])
    higher_MAP_OOC = sum([(after-before)>=0 for (after, before) in zip(l_MAP_after_OOC, l_MAP_before_OOC)])
    higher_MAP_ALL = higher_MAP_IC + higher_MAP_OOC
    lower_MAP_IC = sum([(after-before)<0 for (after, before) in zip(l_MAP_after_IC, l_MAP_before_IC)])
    lower_MAP_OOC = sum([(after-before)<0 for (after, before) in zip(l_MAP_after_OOC, l_MAP_before_OOC)])
    lower_MAP_ALL = lower_MAP_IC + lower_MAP_OOC
    
    higher_SBP_IC = sum([(after-before)>=0 for (after, before) in zip(l_SYSTOLIC_after_IC, l_SYSTOLIC_before_IC)])
    higher_SBP_OOC = sum([(after-before)>=0 for (after, before) in zip(l_SYSTOLIC_after_OOC, l_SYSTOLIC_before_OOC)])
    higher_SBP_ALL = higher_SBP_IC + higher_SBP_OOC
    lower_SBP_IC = sum([(after-before)<0 for (after, before) in zip(l_SYSTOLIC_after_IC, l_SYSTOLIC_before_IC)])
    lower_SBP_OOC = sum([(after-before)<0 for (after, before) in zip(l_SYSTOLIC_after_OOC, l_SYSTOLIC_before_OOC)])
    lower_SBP_ALL = lower_SBP_IC + lower_SBP_OOC
    
    higher_DBP_IC = sum([(after-before)>=0 for (after, before) in zip(l_DIASTOLIC_after_IC, l_DIASTOLIC_before_IC)])
    higher_DBP_OOC = sum([(after-before)>=0 for (after, before) in zip(l_DIASTOLIC_after_OOC, l_DIASTOLIC_before_OOC)])
    higher_DBP_ALL = higher_DBP_IC + higher_DBP_OOC
    lower_DBP_IC = sum([(after-before)<0 for (after, before) in zip(l_DIASTOLIC_after_IC, l_DIASTOLIC_before_IC)])
    lower_DBP_OOC = sum([(after-before)<0 for (after, before) in zip(l_DIASTOLIC_after_OOC, l_DIASTOLIC_before_OOC)])
    lower_DBP_ALL = lower_DBP_IC + lower_DBP_OOC

    print(dz , ": BP # higher, # lower", file=fstream)
    print(higher_MAP_IC, lower_MAP_IC,  file=fstream)
    print(higher_MAP_OOC, lower_MAP_OOC, file=fstream)
    print(higher_MAP_ALL, lower_MAP_ALL, file=fstream)
    print(higher_SBP_IC, lower_SBP_IC, file=fstream)
    print(higher_SBP_OOC, lower_SBP_OOC, file=fstream)
    print(higher_SBP_ALL, lower_SBP_ALL, file=fstream)
    print(higher_DBP_IC, lower_DBP_IC, file=fstream)
    print(higher_DBP_OOC, lower_DBP_OOC, file=fstream)
    print(higher_DBP_ALL, lower_DBP_ALL, file=fstream)


    ## DO K-S test
    print(dz, ": KS test results -----------------------------------------------", file=fstream)
    print("IN CONTROL Mean BP, STD BP, STDERR BP, : Before, After -----------------", file=fstream)
    print("MAP: ", np.mean(l_MAP_before_IC), np.std(l_MAP_before_IC), np.std(l_MAP_before_IC)/len(l_MAP_before_IC), np.mean(l_MAP_after_IC),np.std(l_MAP_after_IC), np.std(l_MAP_before_IC)/len(l_MAP_after_IC), file=fstream)
    print("SYSTOLIC: ", np.mean(l_SYSTOLIC_before_IC), np.std(l_SYSTOLIC_before_IC), np.std(l_SYSTOLIC_before_IC)/len(l_SYSTOLIC_before_IC),np.mean(l_SYSTOLIC_after_IC), np.std(l_SYSTOLIC_after_IC), np.std(l_SYSTOLIC_after_IC)/len(l_SYSTOLIC_after_IC),file=fstream)
    print("DIASTOLIC: ", np.mean(l_DIASTOLIC_before_IC), np.std(l_DIASTOLIC_before_IC), np.std(l_DIASTOLIC_before_IC)/len(l_DIASTOLIC_before_IC),np.mean(l_DIASTOLIC_after_IC), np.std(l_DIASTOLIC_after_IC), np.std(l_DIASTOLIC_after_IC)/len(l_DIASTOLIC_after_IC),file=fstream)
    print("OUT OF CONTROL Mean BP: Before, After", file=fstream)
    print("MAP: ", np.mean(l_MAP_before_OOC), np.std(l_MAP_before_OOC), np.std(l_MAP_before_OOC)/len(l_MAP_before_OOC),np.mean(l_MAP_after_OOC),np.std(l_MAP_after_OOC), np.std(l_MAP_after_OOC)/len(l_MAP_after_OOC), file=fstream)
    print("SYSTOLIC: ", np.mean(l_SYSTOLIC_before_OOC), np.std(l_SYSTOLIC_before_OOC), np.std(l_SYSTOLIC_before_OOC)/len(l_SYSTOLIC_before_OOC),np.mean(l_SYSTOLIC_after_OOC), np.std(l_SYSTOLIC_after_OOC), np.std(l_SYSTOLIC_after_OOC)/len(l_SYSTOLIC_after_OOC),file=fstream)
    print("DIASTOLIC: ", np.mean(l_DIASTOLIC_before_OOC), np.std(l_DIASTOLIC_before_OOC), np.std(l_DIASTOLIC_before_OOC)/len(l_DIASTOLIC_before_OOC),np.mean(l_DIASTOLIC_after_OOC), np.std(l_DIASTOLIC_after_OOC), np.std(l_DIASTOLIC_after_OOC)/len(l_DIASTOLIC_after_OOC),file=fstream)
    print("KS Test: KS Statistic, P-value------------------", file=fstream)
    print("IN CONTROL", file=fstream)
    print("MAP: ", ks_2samp(l_MAP_before_IC, l_MAP_after_IC)[0],  ks_2samp(l_MAP_before_IC, l_MAP_after_IC)[1], file=fstream)
    print("SYSTOLIC: ", ks_2samp(l_SYSTOLIC_before_IC, l_SYSTOLIC_after_IC)[0],  ks_2samp(l_SYSTOLIC_before_IC, l_SYSTOLIC_after_IC)[1], file=fstream)
    print("DIASTOLIC: ", ks_2samp(l_DIASTOLIC_before_IC, l_DIASTOLIC_after_IC)[0],  ks_2samp(l_DIASTOLIC_before_IC, l_DIASTOLIC_after_IC)[1], file=fstream)
    print("OUT OF CONTROL", file=fstream)
    print("MAP: ", ks_2samp(l_MAP_before_OOC, l_MAP_after_OOC)[0],  ks_2samp(l_MAP_before_OOC, l_MAP_after_OOC)[1], file=fstream)
    print("SYSTOLIC: ", ks_2samp(l_SYSTOLIC_before_OOC, l_SYSTOLIC_after_OOC)[0],  ks_2samp(l_SYSTOLIC_before_OOC, l_SYSTOLIC_after_OOC)[1], file=fstream)
    print("DIASTOLIC: ", ks_2samp(l_DIASTOLIC_before_OOC, l_DIASTOLIC_after_OOC)[0],  ks_2samp(l_DIASTOLIC_before_OOC, l_DIASTOLIC_after_OOC)[1], file=fstream)

    ## plots:
    x_OOC = range(len(l_MAP_before_OOC))
    x_IC = range(len(l_MAP_before_IC))
    x_OOC_map = range(50,180)
    x_IC_map = range(50,180)
    x_sbp = range(60, 220)
    x_dbp = range(20, 140)

    fig = plt.figure(1)
    fig.set_size_inches(13,5)
    plt.subplot(121)
    plt.plot(x_IC_map, x_IC_map, 'b', l_MAP_before_IC, l_MAP_after_IC, 'gs')
    plt.xlabel('MAP before')
    plt.ylabel('MAP after')
    plt.title('IN CONTROL')
    plt.subplot(122)
    plt.plot(x_OOC_map, x_OOC_map, 'b', l_MAP_before_OOC, l_MAP_after_OOC, 'rs')
    plt.xlabel('MAP before')
    plt.ylabel('MAP after')
    plt.title('OUT OF CONTROL')
    savestr = output_dir + "plt_strat_" + dz + "_scatter_MAP_before_after_IC_OOC.png"
    fig.savefig(savestr)
    plt.close()

    #plot with both IC and OOC in  the same plot - MAP
    fig = plt.figure(1)
    fig.set_size_inches(8,8)
    plt.plot(x_IC_map, x_IC_map, 'b')
    plt.plot( l_MAP_before_IC, l_MAP_after_IC, 'go')
    plt.plot( l_MAP_before_OOC, l_MAP_after_OOC, 'ro')
    plt.legend(['no change', 'In Control', 'Out of Control'], loc='upper left')
    plt.xlabel('MAP before')
    plt.ylabel('MAP after')
    plt.title('MAP before and after MHT intervention')
    savestr =  output_dir + "plt_strat_" + dz + "_scatter_sameplot_MAP_before_after_IC_OOC.png"
    fig.savefig(savestr)
    plt.close()


    #plot with both IC and OOC in  the same plot - SBP
    fig = plt.figure(1)
    fig.set_size_inches(8,8)
    plt.plot(x_sbp, x_sbp, 'b')
    plt.plot(l_SYSTOLIC_before_IC, l_SYSTOLIC_after_IC, 'go')
    plt.plot(l_SYSTOLIC_before_OOC, l_SYSTOLIC_after_OOC, 'ro')
    plt.legend(['no change', 'In Control', 'Out of Control'], loc='upper left')
    plt.xlabel('Systolic BP before')
    plt.ylabel('Systolic BP after')
    plt.title('Systolic BP before and after MHT intervention')
    savestr =  output_dir + "plt_strat_" + dz + "_scatter_sameplot_SBP_before_after_IC_OOC.png"
    fig.savefig(savestr)
    plt.close()
    

    #plot with both IC and OOC in  the same plot - DBP
    fig = plt.figure(1)
    fig.set_size_inches(8,8)
    plt.plot(x_dbp, x_dbp, 'b')
    plt.plot( l_DIASTOLIC_before_IC, l_DIASTOLIC_after_IC, 'go')
    plt.plot( l_DIASTOLIC_before_OOC, l_DIASTOLIC_after_OOC, 'ro')
    plt.legend(['no change', 'In Control', 'Out of Control'], loc='upper left')
    plt.xlabel('Diastolic BP before')
    plt.ylabel('Diastolic BP after')
    plt.title('Diastolic BP before and after MHT intervention')
    savestr =  output_dir + "plt_strat_" + dz + "_scatter_sameplot_DBP_before_after_IC_OOC.png"
    fig.savefig(savestr)
    plt.close()
    
    
    #P-values: -logP
    fig = plt.figure(2)
    fig.set_size_inches(13,5)
    plt.subplot(121)
    plt.hist(ks_MAP_IC_minsLogP, bins=100, normed=True)
    plt.xlabel('-log(P)')
    plt.ylabel('Probability')
    plt.title('IN CONTROL, n='+ str(len(ks_MAP_IC_minsLogP)))
    plt.subplot(122)
    plt.hist(ks_MAP_OOC_minsLogP, bins=100, normed=True)
    plt.xlabel('-log(P)')
    plt.ylabel('Probability')
    plt.title('OUT OF CONTROL, n=' + str(len(ks_MAP_OOC_minsLogP)))
    savestr =  output_dir + "plt_strat_" + dz + "_hist_MAP_minusLogP_before_after_IC_OOC.png"
    fig.savefig(savestr)
    plt.close()     
    
    #P-values: raw P value: MAP
    fig = plt.figure(2)
    fig.set_size_inches(13,5)
    plt.subplot(131)
    plt.hist(ks_MAP_IC_pval, bins=100, normed=True)
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('IN CONTROL, n='+ str(len(ks_MAP_IC_pval)))
    plt.subplot(132)
    plt.hist(ks_MAP_OOC_pval, bins=100, normed=True)
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('OUT OF CONTROL, n=' + str(len(ks_MAP_OOC_pval)))
    plt.subplot(133)
    plt.hist(np.array( list(ks_MAP_OOC_pval) + list(ks_MAP_IC_pval)), bins=100, normed=True) #concatenage both IC and OOC
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('ALL PATIENTS, n=' + str(len( list(ks_MAP_OOC_pval)+ list(ks_MAP_IC_pval))))
    savestr =  output_dir + "plt_strat_" + dz + "_hist_MAP_Pval_before_after_IC_OOC.png"
    fig.savefig(savestr)
    plt.close()     

    #P-values: raw P value: SBP
    fig = plt.figure(2)
    fig.set_size_inches(13,5)
    plt.subplot(131)
    plt.hist(ks_SBP_IC_pval, bins=100, normed=True)
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('IN CONTROL, n='+ str(len(ks_SBP_IC_pval)))
    plt.subplot(132)

    plt.hist(ks_SBP_OOC_pval, bins=100, normed=True)
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('OUT OF CONTROL, n=' + str(len(ks_SBP_OOC_pval)))
    plt.subplot(133)
    plt.hist(np.array( list(ks_SBP_OOC_pval) + list(ks_SBP_IC_pval)), bins=100, normed=True) #concatenage both IC and OOC
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('ALL PATIENTS, n=' + str(len( list(ks_SBP_OOC_pval) + list(ks_SBP_IC_pval))))
    savestr =  output_dir + "plt_strat_" + dz + "_hist_SBP_Pval_before_after_IC_OOC.png"
    fig.savefig(savestr)
    plt.close()     

    #P-values: raw P value: DBP
    fig = plt.figure(2)
    fig.set_size_inches(13,5)
    plt.subplot(131)
    plt.hist(ks_DBP_IC_pval, bins=100, normed=True)
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('IN CONTROL, n='+ str(len(ks_DBP_IC_pval)))
    plt.subplot(132)
    plt.hist(ks_DBP_OOC_pval, bins=100, normed=True)
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('OUT OF CONTROL, n=' + str(len(ks_DBP_OOC_pval)))
    plt.subplot(133)
    plt.hist(np.array( list(ks_DBP_OOC_pval) + list(ks_DBP_IC_pval)), bins=100, normed=True) #concatenate both IC and OOC
    plt.xlabel('P value')
    plt.ylabel('Probability')
    plt.title('ALL PATIENTS, n=' + str(len( list(ks_DBP_OOC_pval) + list(ks_DBP_IC_pval))))
    savestr =  output_dir + "plt_strat_" + dz + "_hist_DBP_Pval_before_after_IC_OOC.png"
    fig.savefig(savestr)
    plt.close()     

    #sample for an IC patient -- check to see key is in d_bp_before_after_MHT!#######
    print("making sample boxplot for one IC patient")
    from pylab import *
    samp_ruid =  data_BP_stratComorbid[dz]['d_bp_before_after_MHT']['AFTER'].keys()[0] #just take the first key, for now
    samp_map_before = d_bp_before_after_MHT['BEFORE'][samp_ruid]['MAP_list']
    samp_map_after =  d_bp_before_after_MHT['AFTER'][samp_ruid]['MAP_list']
    samp_sbp_before = d_bp_before_after_MHT['BEFORE'][samp_ruid]['SYSTOLIC_list']
    samp_sbp_after =  d_bp_before_after_MHT['AFTER'][samp_ruid]['SYSTOLIC_list']
    samp_dbp_before = d_bp_before_after_MHT['BEFORE'][samp_ruid]['DIASTOLIC_list']
    samp_dbp_after =  d_bp_before_after_MHT['AFTER'][samp_ruid]['DIASTOLIC_list']
    samp_map_before_mean = np.mean(samp_map_before)
    samp_map_after_mean = np.mean(samp_map_after)
    samp_map_before_std = np.mean(samp_map_before)
    samp_map_after_std = np.mean(samp_map_after)
    data = [samp_map_before, samp_map_after, samp_sbp_before, samp_sbp_after, samp_dbp_before, samp_dbp_after]
    fig, ax1 = plt.subplots(figsize=(9,9))
    fig.canvas.set_window_title('Before vs. After Blood Pressure, for one IC patient')
    #boxplot(data)
    plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
    bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax1.set_axisbelow(True)
    ax1.set_title('Before vs. After Blood Pressure, for one IC patient')
    ax1.set_xlabel('BP metric')
    ax1.set_ylabel('Pressure (mmHg)')
    boxColors = ['darkkhaki','royalblue']
    #add labels for "n="
    labels = [ 'MAP Before', 'MAP After', 'SYSTOLIC BP Before', 'SYSTOLIC BP After', 'DIASTOLIC BP Before', 'DIASTOLIC BP After']
    numBoxes = 6
    medians = range(numBoxes)
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        boxCoords = zip(boxX, boxY)
        # Alternate between Dark Khaki and Royal Blue
        k = i % 2
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            plt.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        plt.plot([np.average(med.get_xdata())], [np.average(data[i])],color='w', marker='*', markeredgecolor='k')
    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes+0.5)
    top = max([ max(x) for x in data])/10*10 + 10
    bottom = min([ min(x) for x in data])/10*10 - 10
    plt.yticks(range(bottom,top, 20))
    ax1.set_ylim(bottom, top)
    xtickNames = plt.setp(ax1, xticklabels=labels)
    plt.setp(xtickNames, rotation=45, fontsize=8)
    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes)+1
    upperLabels_n = [ len(samp_map_before), len(samp_map_after), len(samp_sbp_before), len(samp_sbp_after), len(samp_dbp_before), len(samp_dbp_after)]
    upperLabels = [ str('n=' + str(x)) for x in upperLabels_n]
    weights=['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k=tick % 2
        ax1.text(pos[tick], top-(top*0.05), upperLabels[tick],
        horizontalalignment='center', size='x-small', weight=weights[k],
        color=boxColors[k])
    savestr =  output_dir + "plt_strat_" + dz + '_boxplot_samp_MAP_SBP_DBP_IC_ruid_' + str(samp_ruid) + '_before_after.png'
    savefig(savestr)
    
    print("making QQ plots")
    #QQ plot of KS scores - MAP: -logP
    import scipy.stats as stats
    import pylab
    fig = figure()
    fig.set_size_inches(13,5)
    subplot(121)
    stats.probplot(ks_MAP_IC_minsLogP, dist="norm", plot=pylab)
    subplot(122)
    stats.probplot(ks_MAP_OOC_minsLogP, dist="norm", plot=pylab)
    savestr =  output_dir + "plt_strat_" + dz + '_QQplot_KStest_minslogPvals_MAP_IC_OOC.png'
    savefig(savestr)

    #QQ plot of KS scores - MAP: raw Pval
    import scipy.stats as stats
    import pylab
    fig = figure()
    fig.set_size_inches(13,5)
    subplot(121)
    stats.probplot(ks_MAP_IC_pval, dist="norm", plot=pylab)
    subplot(122)
    stats.probplot(ks_MAP_OOC_pval, dist="norm", plot=pylab)
    savestr =  output_dir + "plt_strat_" + dz + '_QQplot_KStest_Pval_MAP_IC_OOC.png'
    savefig(savestr)

    #QQ plot of KS scores - SBP: raw Pval
    import scipy.stats as stats
    import pylab
    fig = figure()
    fig.set_size_inches(13,5)
    subplot(121)
    stats.probplot(ks_SBP_IC_pval, dist="norm", plot=pylab)
    subplot(122)
    stats.probplot(ks_SBP_OOC_pval, dist="norm", plot=pylab)
    savestr =  output_dir + "plt_strat_" + dz + '_QQplot_KStest_Pval_SBP_IC_OOC.png'
    savefig(savestr)

    #QQ plot of KS scores - DBP: raw Pval
    import scipy.stats as stats
    import pylab
    fig = figure()
    fig.set_size_inches(13,5)
    subplot(121)
    stats.probplot(ks_DBP_IC_pval, dist="norm", plot=pylab)
    subplot(122)
    stats.probplot(ks_DBP_OOC_pval, dist="norm", plot=pylab)
    savestr =  output_dir + "plt_strat_" + dz + '_QQplot_KStest_Pval_DBP_IC_OOC.png'
    savefig(savestr)

fstream.close()
