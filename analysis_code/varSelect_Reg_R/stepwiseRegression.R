input_file = '../../../data/new_data_20140416/Data_curated_RC/df_BPSTATUS_Phenotype_BMI_ECG_EGFR_BPCHANGE.csv'

data <- read.table(input_file, header = T, sep=',')

test <- sample(1:202,150,replace=FALSE)


ais0 <- with(ais, data.frame(LBM = LBM, logSSF = log(SSF), logWt = log(Wt), Sex = Sex, logHg=log(Hg), logHt = log(Ht), logRCC = log(RCC), logHc = log(Hc), logWCC = log(WCC), logFerr=log(Ferr)))
ais0 <- as.data.frame(scale(ais0))
m0 <- lm(LBM~1, ais0, subset = test)
m1 <- update(m0,LBM~logWt+logSSF+logRCC+Sex+logHg+logHt+logWCC+logHc+logFerr)
(f <- as.formula(paste("~",paste(names(coef(m1))[-1],collapse="+")))) 
step(m0, scope=list(lower=~1, upper=f), direction="forward")
