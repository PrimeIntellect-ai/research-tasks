You are assisting a researcher who is organizing their dataset evaluation pipelines. We have a Go program `/home/user/pipeline.go` that reads text embeddings from `/home/user/embeddings.csv`, performs feature scaling (Z-score normalization), and evaluates a Nearest Centroid classifier. 

However, the researcher suspects there is a severe data leakage issue: the Z-score normalization (computing the mean and standard deviation) is being performed on the entire dataset *before* splitting it into training and testing sets.

Your task is to fix `/home/user/pipeline.go` to eliminate the data leak. You must modify the code so that:
1. The data is split first (the first 80 rows for training, the last 20 rows for testing).
2. The feature means and standard deviations are calculated **ONLY** on the training data.
3. Both the training and testing data are normalized using the training set's means and standard deviations.
4. The Nearest Centroid classifier is trained on the normalized training data and evaluated on the normalized testing data.

Run your fixed Go program. It should output the corrected test accuracy. Save this exact corrected accuracy (as a decimal number, just the number itself) to `/home/user/fixed_accuracy.txt`.