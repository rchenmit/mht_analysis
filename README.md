mht_analysis
============

MHT program analysis 

* To Load Your Data:
  0. cd analysis_code
  1. python
  2. import pandas as pd
  2.5 modify parse_Phenotype.py: input_folder=/path/to/data and output_dir=/path/to/processed/files
  3. execfile('./parse_Phenotype.py')
  4. repeat step (3) for all parse_*.py files -- this loads all data into Pandas DataFrame objects
  
* My analysis so far:
  1. newdata_analysis_wrapper.py
