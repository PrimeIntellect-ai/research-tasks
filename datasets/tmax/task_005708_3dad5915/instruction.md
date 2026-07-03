You are an MLOps engineer testing the behavior of model embeddings across two different training runs. The embeddings are stored as artifacts, and you need to determine if the dominant feature representations have statistically shifted between the runs.

You have two embedding datasets located at:
- `/home/user/artifacts/run_alpha.csv`
- `/home/user/artifacts/run_beta.csv`
These files contain comma-separated numerical data with no header.

Your task is to write and run a Python script that performs the following steps:
1. **Numerical Library Configuration**: Globally set the NumPy random seed to `42`. Configure NumPy to raise an exception on *all* floating-point errors (e.g., divide by zero, overflow) to simulate our strict CI testing environment.
2. **Data Preparation**: Load both CSV files. Concatenate them with `run_alpha` first, followed by `run_beta`, to create a single combined dataset.
3. **Preprocessing**: Standardize the combined dataset so that each feature has a mean of 0 and a variance of 1 using `sklearn.preprocessing.StandardScaler`.
4. **Dimensionality Reduction**: Apply PCA to the standardized combined dataset to reduce it to 2 dimensions. Set `random_state=42` in the PCA model.
5. **Separation**: Split the transformed (2D) dataset back into the `alpha` and `beta` groups.
6. **Hypothesis Testing**: Perform Welch's t-test (independent 2-sample t-test with unequal variances) on the **first principal component (PC1)** to compare the `alpha` group against the `beta` group.
7. **Reporting**: Create a JSON file at `/home/user/report.json` containing exactly the following keys:
   - `"pc1_variance_ratio"`: The explained variance ratio of the first principal component (float).
   - `"t_statistic"`: The t-statistic calculated from Welch's t-test (float).
   - `"p_value"`: The two-sided p-value from the test (float).
   - `"reject_null"`: A boolean (`true` or `false`) indicating if the null hypothesis (that the two independent samples have identical average expected values) is rejected at a significance level of 0.05.

Ensure your JSON outputs standard float values. Do not round the floats yourself; let Python's `json.dump` handle the default precision.