## wrapper

## path
#workingDir= '/home/orbit/Dropbox/GT/GT_Sunlab/med_status/ANALYSIS_FULL_DATASET/code/'
#sys.path.append('C:\\anaconda\\lib\\site-packages')

#workingDir = 'C:\\Users\\Thinkpad\\Dropbox\\GT\\GT_Sunlab\\med_status\\ANALYSIS_FULL_DATASET\\code'
workingDir = './';
pickleDir = 'workingDir\\pickle_20140306_7pm'


## import these
import os
import sys

if os.name == 'nt': #'nt' = windows
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

## run data processing
#execfile('newdata_dataread_BP_MHTSTRATEGY_v1.py')
#execfile('newdata_analyzeBP_BP_MHTSTRATEGY.py')
execfile('newdata_make_list_pts_IN_OUT.py')
execfile('./KS_2samp_test_before_after_MHT.py')
execfile('./KS_2samp_test_before_after_MHT_stratComorbid.py')

## run pymining
#execfile('pymining_play.py')
#execfile('mlpy_build_features.py')
#execfile('generate_statistics_for_table.py')
