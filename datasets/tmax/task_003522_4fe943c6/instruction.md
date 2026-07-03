You are a Machine Learning Engineer preparing a training dataset. You have discovered a systematic shift in your sensor data, and you need to align it with a reference distribution before feeding it into your models. 

Your task is to build a reproducible data transformation pipeline in **Rust** that finds the optimal parameters to transform the raw data so it matches the reference data distribution as closely as possible.

**Data:**
You have two files:
1. `/home/user/raw_data.csv`: Contains a single column `x` (float64) representing the raw sensor readings.
2. `/home/user/ref_data.csv`: Contains a single column `z` (float64) representing the reference distribution.

**Transformation:**
Apply the polynomial transformation: 
$y_i = \alpha x_i^2 + \beta x_i$

**Objective:**
Find the parameters $\alpha$ and $\beta$ that minimize the two-sample Kolmogorov-Smirnov (KS) statistic between the transformed dataset $Y$ and the reference dataset $Z$. The two-sample KS statistic is defined as the maximum absolute difference between the empirical cumulative distribution functions (CDFs) of the two samples.

**Optimization Specification:**
To ensure strict reproducibility in the pipeline, perform a Grid Search optimization over the following parameter space:
- $\alpha \in [0.0, 1.0]$ with a step size of exactly `0.05` (inclusive of bounds, so 0.0, 0.05, 0.10, ..., 1.0).
- $\beta \in [0.0, 2.0]$ with a step size of exactly `0.10` (inclusive of bounds).

When evaluating the KS statistic, if there is a tie (multiple parameter pairs yielding the exact same minimum KS statistic), select the pair with the smallest $\alpha$, and then the smallest $\beta$.

**Requirements:**
1. Initialize a new Rust binary project at `/home/user/data_prep`.
2. You may use external crates (like `csv`, `serde`, `statrs`) by adding them to your `Cargo.toml`.
3. Your Rust program must read the CSVs, perform the parameter grid search, and compute the 2-sample KS test for each combination.
4. The program must output the best parameters and the corresponding KS statistic to a JSON file at `/home/user/results.json` with the following exact format:
```json
{
  "alpha": 0.55,
  "beta": 1.20,
  "ks_stat": 0.123456
}
```
*(Note: Round the output numbers in the JSON to 2 decimal places for alpha/beta, and 6 decimal places for ks_stat, using standard half-up rounding).*
5. Write a shell script at `/home/user/run_pipeline.sh` that compiles the Rust project in release mode and executes it. Make it executable. Run this script to generate the final `results.json`.