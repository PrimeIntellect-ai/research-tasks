You are an MLOps engineer investigating a recent degradation in model evaluation metrics. 

You have a directory `/home/user/experiments` containing 10 CSV files (`run_01.csv` to `run_10.csv`), representing prediction logs from different model runs. 

Recently, a silent data pipeline bug was introduced: in some runs, missing values (NaNs) were injected into the `text_token_id` column. Because pandas casts integer columns with NaNs to floats, these corrupted runs have `text_token_id` stored as floats (with some empty values in the CSV), while healthy runs have them as pure integers. This bug inadvertently ruined the tokenization alignment, causing poor model predictions.

Your task is to audit these artifacts, calculate the impact, and perform a statistical bootstrap analysis.

Specifically, write and execute a Python script to do the following:
1. Identify all "corrupted" runs (files where `text_token_id` is parsed as float due to the presence of missing/NaN values) vs "clean" runs (where `text_token_id` has no missing values and can be represented as integers).
2. Combine all clean runs into one DataFrame, and all corrupted runs into another DataFrame.
3. Calculate the Pearson correlation coefficient between `true_label` and `predicted_prob` for the combined clean runs (`uncorrupted_corr`).
4. Calculate the Pearson correlation coefficient between `true_label` and `predicted_prob` for the combined corrupted runs (`corrupted_corr`).
5. Perform a bootstrap analysis on the **combined clean runs** to find the 95% confidence interval of the correlation coefficient:
    - Use 1000 bootstrap iterations.
    - In each iteration, sample with replacement a dataset of the same size as the combined clean dataset.
    - Use `numpy.random.seed(42)` immediately before starting the loop of 1000 iterations to ensure reproducibility.
    - Calculate the 2.5th and 97.5th percentiles of the bootstrapped correlations using `numpy.percentile`.

Save your final results in a JSON file at `/home/user/audit_report.json` with the exact following structure:
```json
{
  "corrupted_runs": ["run_XX.csv", "run_YY.csv"],
  "uncorrupted_corr": 0.12345,
  "corrupted_corr": 0.12345,
  "bootstrap_ci_lower": 0.12345,
  "bootstrap_ci_upper": 0.12345
}
```
*Note: Sort the `corrupted_runs` list alphabetically. Round all float values to 5 decimal places.*