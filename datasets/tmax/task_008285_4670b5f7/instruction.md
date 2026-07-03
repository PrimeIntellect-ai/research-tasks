You are a machine learning engineer tasked with preparing and validating a new batch of training data. You need to ensure that the new multi-dimensional sensor readings ("candidate dataset") do not suffer from severe covariate shift compared to a gold-standard "reference dataset".

To evaluate this, you must compare the datasets using Kernel Density Estimation (KDE) and compute bootstrap confidence intervals for the mean log-likelihood of the candidate data under the reference distribution.

You have been provided with two files in your home directory:
1. `/home/user/reference_data.npy`: A 2D numpy array representing the reference dataset.
2. `/home/user/candidate_data.npy`: A 2D numpy array representing the new candidate dataset.

Write and execute a Python script to perform the following steps:
1. Load both `.npy` datasets.
2. Fit a Kernel Density Estimator to `reference_data.npy`. You must use `sklearn.neighbors.KernelDensity` with a `'gaussian'` kernel and `bandwidth=0.5`.
3. Compute the log-likelihood of each sample in `candidate_data.npy` using the fitted KDE (using `score_samples`).
4. Calculate the mean log-likelihood of the candidate samples.
5. Perform bootstrap resampling to find the 95% confidence interval of this mean log-likelihood:
   - Use exactly `1000` bootstrap iterations.
   - In each iteration, sample with replacement from the candidate log-likelihoods (the sample size should equal the size of the candidate dataset).
   - Compute the mean for each resampled dataset.
   - **Crucial:** To ensure reproducibility, you must call `numpy.random.seed(42)` exactly once, immediately before starting your 1000-iteration bootstrap loop.
   - Calculate the 2.5th and 97.5th percentiles of the 1000 bootstrapped means using `numpy.percentile`.
6. Save the results to a JSON file at `/home/user/distribution_metrics.json`. The JSON file must have exactly the following keys, with values rounded to exactly 4 decimal places:
   - `"mean_ll"`: The mean log-likelihood of the original candidate dataset.
   - `"ci_lower"`: The 2.5th percentile of the bootstrapped means.
   - `"ci_upper"`: The 97.5th percentile of the bootstrapped means.

Ensure your environment has the necessary libraries (e.g., `scikit-learn`, `numpy`). You may install them via `pip` if they are missing.