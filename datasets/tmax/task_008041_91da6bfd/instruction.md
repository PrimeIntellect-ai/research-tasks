You are an ML Engineer preparing robust statistical baselines for a new anomaly detection model. A previous script meant to extract data and calculate variance metrics failed, producing NaN values due to a misconfiguration in how it handled matrix operations and empty data batches. 

Your task is to write a new Python script from scratch at `/home/user/bootstrap_pca.py` that performs the following pipeline:

1. **ETL**: Read the dataset located at `/home/user/sensor_data.csv`. Filter the dataset to keep only the rows where the `sensor_state` column equals `'ACTIVE'`. Extract only the feature columns: `f1`, `f2`, and `f3`.
2. **Sampling**: Perform exactly 1000 bootstrap resamples (sampling *with replacement*) of this filtered dataset. Each bootstrap sample must have the same number of rows as the filtered dataset. 
   *IMPORTANT*: To ensure reproducibility, set `numpy.random.seed(42)` immediately before starting your bootstrap loop, and use `numpy.random.choice` to generate the row indices for your samples.
3. **Linear Algebra (Variance Analysis)**: For each of the 1000 bootstrap samples, calculate the unbiased covariance matrix of the 3 features (features are columns). Then, compute the largest eigenvalue of this covariance matrix.
4. **Output**: Calculate the mean of these 1000 largest eigenvalues. Save this single mean value to a file named `/home/user/eigen_baseline.txt`, rounded to exactly 4 decimal places (e.g., `12.3456`).

Ensure your script runs successfully and creates the requested output file.