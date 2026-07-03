You are a data analyst taking over a project where a data leakage issue was discovered. 

A previous analyst was working with two files: `/home/user/train.csv` and `/home/user/test.csv`. They standardized the test set improperly by using the test set's *own* means and standard deviations, rather than using the training set's parameters. This resulted in data leakage.

Your task is to quantify the impact of this leakage using Python. Write a script that performs the following steps:

1. Read the tabular data from `/home/user/train.csv` and `/home/user/test.csv`. Both files have columns: `feature_1`, `feature_2`, `feature_3`.
2. Compute the **incorrectly standardized** test set. For each column, subtract the mean of that column in `test.csv` and divide by the population standard deviation (ddof=0) of that column in `test.csv`.
3. Compute the **correctly standardized** test set. For each column in `test.csv`, subtract the mean of that corresponding column in `train.csv` and divide by the population standard deviation (ddof=0) of that column in `train.csv`.
4. Perform an independent 2-sample t-test (Welch's t-test, assuming unequal variances) comparing the `feature_1` values of the *incorrectly standardized* test set against the `feature_1` values of the *correctly standardized* test set.
5. Using linear algebra concepts, calculate the dot product between the *correctly standardized* `feature_1` vector and the *correctly standardized* `feature_2` vector from the test set.
6. Save your final metrics to `/home/user/leakage_report.json`. The JSON file must have exactly this structure (round all numeric values to 4 decimal places):
```json
{
  "t_statistic": 1.2345,
  "p_value": 0.1234,
  "dot_product": 12.3456
}
```

Ensure your script handles everything programmatically and produces the exact file requested.