#hierarchical clustering

library(stats)

names_cluster_features <- l_features_for_cluster
cluster_features <- data_for_model_scaled[, names_cluster_features]
cluster_features.dist <- dist(cluster_features)
cluster_features.hclust <- hclust(cluster_features.dist)
