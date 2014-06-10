## select subsets from data
source('load_data.R')



subset1 <- subset(data_for_model_not_scaled, X249.250.99>=1, select=change_EGFR)