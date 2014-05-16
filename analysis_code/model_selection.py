## Robert Chen
## Monday 5/12/2014
##
## model selection for partitioning patients --> to predict whether or not the program worked
##
## ASSUMES that CSV files have been processed! (BMI, Phenotype, etc)
## Parameters:
##  *Age, sex, BMI, etc
##
##

## Process data into lists


## toy example
clfLasso = linear_model.lasso(alpha = 0.1)
l_subjects = []
for i in range(len(df_BMI_aggregate)):
    this_list = [ df_BMI_aggregate.ix[i]['change_BMI'], df_BMI_aggregate.ix[i]['BMI'] ]
    l_subjects.append(this_list)
nparr_subjects = np.array(df_BMI_aggregate.ix[0:4, ['change_BMI', 'BMI']])
l_targets = list(df_BMI_aggregate.ix[0:4]['BMI'])

## Run Lasso
clfLasso.fit(nparr_subjects, l_targets)
print clfLasso.coef_


## Stepwise regression, AFTER regularizing with Lasso


