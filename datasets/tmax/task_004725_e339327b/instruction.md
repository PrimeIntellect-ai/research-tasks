You are a bioinformatics analyst tasked with evaluating k-mer sequence distributions to classify microbial samples into two groups. 

You have been provided with the following files in `/home/user/`:
- `kmer_train.npy`: A 2D NumPy array containing k-mer frequency counts for the training samples (rows are samples, columns are k-mers).
- `labels_train.npy`: A 1D NumPy array containing the binary group labels (0 or 1) for the training samples.
- `kmer_test.npy`: A 2D NumPy array containing k-mer frequency counts for the test samples.
- `labels_test.npy`: A 1D NumPy array containing the binary group labels for the test samples.

Your task is to build and evaluate a predictive model using the following exact pipeline:

1. **Normalization**: For both training and test data, normalize the k-mer counts so that each sample (row) sums to 1.0. This converts the counts into probability distributions.
2. **Distribution Distance**: Calculate the Jensen-Shannon distance (using `scipy.spatial.distance.jensenshannon`) between the mean probability distribution of Group 0 and the mean probability distribution of Group 1 from the *training* set. Save this distance rounded to 4 decimal places in `/home/user/js_distance.txt`.
3. **Dimensionality Reduction**: Center the normalized training data by subtracting the column means. Perform Singular Value Decomposition (SVD) on this centered training matrix using `numpy.linalg.svd`. Extract the top 5 right singular vectors. Project both the centered training data and the centered test data (using the training column means) onto these 5 components.
4. **Modeling**: Fit a standard Logistic Regression model (using `sklearn.linear_model.LogisticRegression` with default parameters and `random_state=42`) on the 5-dimensional projected training data to predict the labels.
5. **Prediction & Statistical Comparison**: Predict the probability of belonging to Group 1 for all samples in the *test* set. Perform Welch's t-test (`scipy.stats.ttest_ind` with `equal_var=False`) comparing the predicted probabilities for the true Group 1 test samples versus the true Group 0 test samples. Save the resulting p-value in scientific notation with 2 decimal places (e.g., `1.23e-04`) to `/home/user/ttest_pvalue.txt`.