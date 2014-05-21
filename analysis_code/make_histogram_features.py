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

print("running ./make_histogram_features.py")
output_file = '../analysis_output/make_histogram_features.out'
output_dir = '../analysis_output/'


## plots:


#BMI data; plot histo -- all ENTRIES
fig = plt.figure(2)
fig.set_size_inches(20,8)
plt.subplot(131)
plt.hist(df_BMI[isnan(df_BMI['BMI'])==False]['BMI'], normed=True, bins=10)
plt.xlabel('BMI')
plt.ylabel('#')
plt.title('BMI, n='+ str(len(df_BMI.BMI)))
plt.subplot(132)
plt.hist(df_BMI[isnan(df_BMI['Height'])==False]['Height'], normed=True, bins = 10)
plt.xlabel('Height')
plt.ylabel('#')
plt.title('Height(cm), n=' + str(len(df_BMI.Height)))
plt.subplot(133)
plt.hist(df_BMI[isnan(df_BMI['Weight'])==False]['Weight'], normed=True, bins = 10)
plt.xlabel('Weight')
plt.ylabel('#')
plt.title('Weight(kg), n=' + str(len(df_BMI.Weight)))

fig.savefig(output_dir + "plt_hist_BMI_Height_Weight.png")
plt.close()     



#BMI data; plot histogram CUMSUM-- all ENTRIES
fig = plt.figure(2)
fig.set_size_inches(20,8)
plt.subplot(131)
values, base = np.histogram(df_BMI[isnan(df_BMI['BMI'])==False]['BMI'], bins = 50)
cumulative = np.cumsum(values)
plt.plot(base[:-1], cumulative)
plt.xlabel('BMI')
plt.ylabel('#')
plt.title('BMI, n='+ str(len(df_BMI.BMI)))
plt.subplot(132)
values, base = np.histogram(df_BMI[isnan(df_BMI['BMI'])==False]['Height'], bins = 50)
cumulative = np.cumsum(values)
plt.plot(base[:-1], cumulative)
plt.xlabel('Height')
plt.ylabel('#')
plt.title('Height(cm), n=' + str(len(df_BMI.Height)))
plt.subplot(133)
values, base = np.histogram(df_BMI[isnan(df_BMI['BMI'])==False]['Weight'], bins = 50)
cumulative = np.cumsum(values)
plt.plot(base[:-1], cumulative)
plt.xlabel('Weight')
plt.ylabel('#')
plt.title('Weight(kg), n=' + str(len(df_BMI.Weight)))

fig.savefig(output_dir + "plt_hist_cdf_BMI_Height_Weight.png")
plt.close()     


#BMI data; plot histogram of AVG BMI
fig = plt.figure(2)
fig.set_size_inches(20,8)
plt.subplot(131)
data = df_BMI_aggregate[isnan(df_BMI_aggregate['AVG_BMI'])==False]['AVG_BMI']
plt.hist(data , normed=True, bins=100)
plt.xlabel('BMI')
plt.ylabel('#')
plt.title('BMI, n='+ str(len(data)))
plt.subplot(132)
data = df_BMI_aggregate[isnan(df_BMI_aggregate['AVG_HEIGHT'])==False]['AVG_HEIGHT']
plt.hist(data, normed=True, bins = 100)
plt.xlabel('Height')
plt.ylabel('#')
plt.title('Height(cm), n=' + str(len(data)))
plt.subplot(133)
data = df_BMI_aggregate[isnan(df_BMI_aggregate['AVG_WEIGHT'])==False]['AVG_WEIGHT']
plt.hist( data , normed=True, bins = 100)
plt.xlabel('Weight')
plt.ylabel('#')
plt.title('Weight(kg), n=' + str(len(data)))

fig.savefig(output_dir + "plt_hist_BMI_aggregate_AVG_BMI_Height_Weight.png")
plt.close()     


#histogram of change in BP: 
fig = plt.figure(2)
fig.set_size_inches(20,8)
plt.subplot(131)
data = df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE[isnan(df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE['MEDIAN_SYSTOLIC_CHANGE'])==False]['MEDIAN_SYSTOLIC_CHANGE']
plt.hist(data , bins=100)
plt.xlabel('change in systolic pressure')
plt.ylabel('#')
plt.title('Systolic BP, n='+ str(len(data)))
plt.subplot(132)
data = df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE[isnan(df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE['MEDIAN_DIASTOLIC_CHANGE'])==False]['MEDIAN_DIASTOLIC_CHANGE']
plt.hist(data, bins = 100)
plt.xlabel('change in diastolic pressure')
plt.ylabel('#')
plt.title('Diastolic BP, n=' + str(len(data)))
plt.subplot(133)
data =  df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE[isnan(df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE['MEDIAN_MAP_CHANGE'])==False]['MEDIAN_MAP_CHANGE']
plt.hist( data , bins = 100)
plt.xlabel('change in MAP')
plt.ylabel('#')
plt.title('MAP, n=' + str(len(data)))

fig.savefig(output_dir + "plt_hist_BP_change_SBP_DBP_MAP_ALLPATIENTS.png")
plt.close()     
