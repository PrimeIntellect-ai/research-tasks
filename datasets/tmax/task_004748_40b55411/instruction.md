You are an ML Engineer preparing training data. You have a high-dimensional dataset of uncleaned embeddings, and you need to reduce its dimensionality and remove outliers using a probabilistic approach before downstream model training. 

We want this process to be deterministic and reproducible. Complete the following tasks in Python:

1. **Numerical Library Configuration**: Before running your data processing code, ensure that your environment is strictly single-threaded to prevent non-determinism in some numerical libraries. Set the environment variables `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`.
2. **Data Loading**: Load the raw data from `/home/user/raw_embeddings.npy` (shape: `1000` samples, `50` features).
3. **Dimensionality Reduction**: Use `sklearn.decomposition.PCA` to reduce the dataset from 50 down to 10 components. Initialize PCA with `random_state=42`.
4. **Bayesian Inference for Outlier Detection**: On the 10-dimensional PCA-reduced data, fit a Bayesian Gaussian Mixture Model using `sklearn.mixture.BayesianGaussianMixture`. 
    - Set `n_components=5`.
    - Set `random_state=42`.
    - Set `max_iter=500`.
    - Once fitted, score each sample to get its log-likelihood (use the `.score_samples()` method).
5. **Data Cleaning**: Filter out the samples that have the lowest log-likelihoods. Specifically, identify and remove the bottom 5% (i.e., the 50 samples with the lowest scores).
6. **Output**:
    - Save the cleaned, 10-dimensional numpy array (which should have exactly 950 samples) to `/home/user/clean_embeddings.npy`.
    - Save the original integer row indices of the 50 removed outliers (relative to the original 1000-row array) to `/home/user/outliers.txt`. The text file should contain one integer index per line, sorted in ascending order.