You are a data analyst tasked with processing sensor data to perform mathematical and statistical analysis. 

You have been provided with a dataset at `/home/user/sensor_data.csv` containing the following columns: `time`, `temp`, `pressure`, `humidity`, and `vibration`.

Your objective is to create a Bash shell script at `/home/user/run_analysis.sh` that orchestrates the following data science pipeline. You may write inline Python code (using heredocs or `python3 -c`) within the Bash script to handle complex math, but the entry point must be the Bash script.

The pipeline must perform the following tasks:
1. **Correlation Analysis**: Calculate the Pearson correlation coefficient between `temp` and `pressure`.
2. **Bootstrap Sampling**: Perform 1000 bootstrap iterations (sampling with replacement) on the `temp` and `pressure` pairs to compute the 5th and 95th percentiles of the Pearson correlation coefficient, forming a 90% confidence interval.
3. **Cross-Validation & Hyperparameter Tuning**: Train a Ridge regression model to predict `vibration` using `temp`, `pressure`, and `humidity` as features. Use 5-fold cross-validation to evaluate three candidate `alpha` (regularization) values: 0.1, 1.0, and 10.0. Select the `alpha` that yields the lowest Mean Squared Error (MSE).

**Requirements & Constraints**:
- Set the random seed to `42` for all random operations (bootstrap sampling, K-Fold splitting, etc.) to ensure reproducibility.
- For cross-validation, use an exact 5-fold split with shuffling enabled (`random_state=42`).
- The Bash script should output a JSON file at `/home/user/results.json` with exactly the following structure (values rounded to 4 decimal places):

```json
{
  "correlation": 0.8521,
  "bootstrap_ci_5th": 0.8210,
  "bootstrap_ci_95th": 0.8810,
  "best_alpha": 1.0
}
```

Ensure your script `/home/user/run_analysis.sh` is executable and generates `/home/user/results.json` when run without any arguments.