You are a data analyst tasked with processing a noisy dataset of sensor readings. You need to enforce a data schema, perform a bootstrap analysis, and use linear algebra/dimensionality reduction techniques to estimate the stability of the primary signal in the data.

Your input file is located at: `/home/user/sensor_data.csv`

Please write and run a Python script to perform the following pipeline:

1. **Schema Enforcement**: Read `/home/user/sensor_data.csv`. The schema expects 10 feature columns named `s1` through `s10`. 
   - Force these 10 columns to be of numeric (float) type.
   - Any values that cannot be parsed as numbers (e.g., error strings) should be coerced to NaN.
   - Drop any rows that contain NaN values in any of these 10 columns.

2. **Bootstrap Sampling**: You will estimate the stability of the variance explained by the first principal component (PC1).
   - Perform 500 bootstrap iterations.
   - For each iteration `i` (where `i` ranges from 0 to 499 inclusive), generate a bootstrap sample of the cleaned data by sampling with replacement. **Crucial:** Use pandas `df.sample(n=len(cleaned_df), replace=True, random_state=i)` so the results are exactly reproducible.

3. **Dimensionality Reduction (Linear Algebra)**: For each of the 500 bootstrap samples:
   - Center the sample (subtract the mean of each column).
   - Compute the covariance matrix.
   - Compute the eigenvalues of the covariance matrix.
   - Calculate the proportion of total variance explained by the first principal component (the largest eigenvalue divided by the sum of all eigenvalues).

4. **Reporting**: Calculate the mean, the 2.5th percentile (lower confidence interval), and the 97.5th percentile (upper confidence interval) of the PC1 explained variance across the 500 iterations.
   
Save the results as a JSON file at `/home/user/pca_stability.json` with exactly the following keys and format, rounding the float values to 4 decimal places:
```json
{
  "mean_pc1_var": 0.1234,
  "ci_lower": 0.1234,
  "ci_upper": 0.1234
}
```