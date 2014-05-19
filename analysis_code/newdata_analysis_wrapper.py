## wrapper

## set these options
workingDir = './';
bool_initial_run = 0


## import these
import os
import sys

if os.name == 'nt': #'nt' = my windows machine
    sys.path.append('C:\\anaconda\\lib\\site-packages')
if os.name == 'posix': #PACE server monkeys.pace.gatech.edu
    sys.path.append('/nv/hcoc1/rchen87/anaconda/lib/python2.7/site-packages')
    
import pandas as pd
import numpy as np
import math
import copy
import csv
import scipy as s
import openpyxl
from openpyxl import load_workbook
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
from collections import Counter
#import pickle
if sys.version_info.major == 3:
    import pickle
else:
    import cPickle as pickle


os.chdir(workingDir)
sys.path.append('./')

## run these scripts: ---------------------------------------------------------------------------------

if bool_initial_run:
    # read in and process data
    execfile('newdata_dataread_BP_MHTSTRATEGY_v2.py')
    # analyze BP intervals to determine IN CONTROL / OUT OF CONTROL status
    execfile('newdata_analyzeBP_BP_MHTSTRATEGY.py')
    #parse other files
    execfile('parse_Phenotype.py')
    execfile('parse_BMI.py')
    execfile('parse_ECG.py')
    execfile('parse_EGFR.py')
    execfile('parse_BP.py')
    execfile('parse_ICD.py')
    execfile('parse_CPT.py')
    # make lists of patients IN control or OUT of control for HYPERTENSION set
    execfile('newdata_make_list_pts_IN_OUT.py')
    # KS test, etc for patients in the HYPERTENSION set
    execfile('./KS_2samp_test_before_after_MHT.py')
    # KS test, etc for patients in the other MHT comorbities: DIABETES and CHF sets
    execfile('./KS_2samp_test_before_after_MHT_stratComorbid.py')

if not bool_initial_run:
    execfile('load_saved_pickles.py')
    execfile('parse_Phenotype.py')
    execfile('parse_BMI.py')
    execfile('parse_ECG.py')
    execfile('parse_EGFR.py')
    execfile('parse_BP.py')
    execfile('parse_ICD.py')
    execfile('parse_CPT.py')
    execfile('newdata_make_list_pts_IN_OUT.py')
    execfile('./KS_2samp_test_before_after_MHT.py')

