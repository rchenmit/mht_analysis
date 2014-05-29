## set python path and import modules;

## set default to anaconda

## import modules
import os
import sys
if os.name == 'nt': #'nt' = windows                                                                                                                                                                                        
    sys.path.append('C:\\anaconda\\lib\\site-packages') #in windows, alot of modules were installed with Anaconda
if os.name == 'posix': #PACE cluster
    #sys.path.append('/nv/hcoc1/rchen87/anaconda/lib/python2.7/site-packages') #put anaconda at the FRONT of the path        
    sys.path[0] = '/nv/hcoc1/rchen87/anaconda/lib/python2.7/site-packages'
    sys.path.insert(0, '') # this is a python standard; null string at start of path array
import xlrd #needed for reading in the XLS file with python
import pandas as pd
import numpy as np
import math 
import copy
import csv
import scipy as s
#import openpyxl
#from openpyxl import load_workbook
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

