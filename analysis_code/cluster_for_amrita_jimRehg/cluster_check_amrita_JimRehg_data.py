import os 
import sys
import pandas as pd

os.chdir("/Users/localadmin/HTN_Predictive/github_mht_analysis/analysis_code/cluster_for_amrita_jimRehg/")

df_MHT_RUID_cluster = pd.read_csv("./df_MHT_RUID_cluster.csv")

df_BP_from_amrita = pd.read_csv("./BP.csv", sep='\t')

l_pts_amrita = list(df_BP_from_amrita.RUID.unique())
l_pts_rchen = list(df_MHT_RUID_cluster.RUID.unique())