You are a data scientist analyzing an unknown dataset. You need to determine whether the data is better modeled by a Normal distribution or a Laplace distribution by explicitly fitting both distributions using optimization and comparing their goodness-of-fit.

Your task is to:
1. Read the dataset from `/home/user/data.txt`. This file contains a single column of 500 continuous values.
2. Define an objective function that computes the Kolmogorov-Smirnov (KS) statistic (representing the maximum distance between the empirical CDF and theoretical CDF) between the data and a Normal distribution parameterized by `[mu, sigma]`.
3. Use the Nelder-Mead optimization algorithm to minimize this objective function and find the optimal `[mu, sigma]` that minimizes the KS distance. To ensure numerical stability, initialize the optimization with the sample mean and sample standard deviation of the data.
4. Repeat this process to fit a Laplace distribution parameterized by `[loc, scale]`. Minimize the KS statistic between the data and the Laplace CDF. Initialize the Nelder-Mead optimization with the sample median and sample standard deviation of the data.
5. Compare the two hypotheses by checking which optimal distribution yields the lowest KS distance.
6. Save your results to `/home/user/results.json` with exactly the following keys and format:

```json
{
    "normal_params": [mu, sigma],
    "normal_ks_distance": 0.0000,
    "laplace_params": [loc, scale],
    "laplace_ks_distance": 0.0000,
    "best_fit": "Normal"
}
```

Constraints:
- All numerical values in the output JSON must be rounded to exactly 4 decimal places.
- The `best_fit` value must be either `"Normal"` or `"Laplace"`.
- Use an optimization routine (e.g., `scipy.optimize.minimize` in Python) rather than maximum likelihood estimators, as you are specifically tasked with minimizing the KS distance.