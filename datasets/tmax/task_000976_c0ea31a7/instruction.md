You are an MLOps engineer tracking feature extraction experiments. We have run three different feature engineering pipelines, producing three artifact datasets. You need to analyze the generalized variance of these features under a Bayesian probabilistic framework to select the most informative, yet stable, feature set.

Your task is to write a C++ program that processes these experiment artifacts, computes a regularized covariance matrix for each, calculates the determinant (generalized variance), and logs the experiment tracking results.

**Data Location:**
There are three CSV files located in `/home/user/experiments/`:
1. `exp_alpha.csv`
2. `exp_beta.csv`
3. `exp_gamma.csv`

Each file contains 10 rows and 3 columns of floating-point numbers representing the extracted features for a batch of samples. There is no header row.

**Processing Requirements:**
Write a C++ program (e.g., `/home/user/evaluate_experiments.cpp`) using only the standard library that does the following for each CSV:
1. Parse the CSV into a 2D array or vector of vectors.
2. Compute the $3 \times 3$ sample covariance matrix $\Sigma$. Use $N-1$ in the denominator (where $N=10$ is the number of rows).
3. Apply a Bayesian prior to regularize the covariance matrix. Compute $\Sigma' = \Sigma + \lambda I$, where $\lambda = 0.1$ and $I$ is the $3 \times 3$ identity matrix.
4. Compute the determinant of $\Sigma'$. This is our metric for regularized generalized variance.

**Tracking Output:**
Your program (or a wrapper script using your compiled C++ program) must output a tracking file at `/home/user/tracker.json`.
The JSON file must have exactly this format:
```json
{
  "exp_alpha": <determinant_alpha_rounded_to_4_decimal_places>,
  "exp_beta": <determinant_beta_rounded_to_4_decimal_places>,
  "exp_gamma": <determinant_gamma_rounded_to_4_decimal_places>,
  "best": "<name_of_experiment_with_LOWEST_determinant>"
}
```
*Note: Use standard half-up rounding to 4 decimal places for the numeric values in the JSON.*

Compile and run your C++ code to generate `/home/user/tracker.json`.