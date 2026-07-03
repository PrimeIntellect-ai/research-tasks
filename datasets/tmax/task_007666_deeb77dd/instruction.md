You are a data scientist working on a legacy system where standard data science libraries (like Python's pandas or scikit-learn) are unavailable, and all automated data cleaning pipelines must be written in Bash (using standard UNIX utilities like `awk`, `sed`, `grep`).

You have a dataset at `/home/user/raw_data.csv` containing sensor readings. The columns are `id,value,label,fold`.
- `id`: Integer identifier.
- `value`: Floating point sensor reading.
- `label`: 0 for normal, 1 for known anomaly.
- `fold`: An integer (1, 2, or 3) indicating the cross-validation fold.

Your task is to write a Bash script `/home/user/clean_pipeline.sh` that implements a simple Gaussian probabilistic anomaly detector, tunes its hyperparameter using cross-validation, and selects the best threshold.

**Step 1: Cross-Validation & Hyperparameter Tuning**
You need to tune a threshold multiplier `T` to detect anomalies. The candidate values for `T` are `2`, `3`, and `4`.
For each `T`:
Perform 3-fold cross-validation. For each fold `k` in {1, 2, 3}:
1. **Train**: Filter the data where `fold != k` AND `label == 0`. Compute the mean ($\mu$) and sample standard deviation ($s$) of the `value` column. (If the variance is 0, assume $s=0.0001$).
2. **Test**: For all rows where `fold == k`, predict an anomaly (prediction=1) if $|value - \mu| > T \times s$, otherwise predict 0.
3. **Evaluate**: Calculate the accuracy on fold `k` (number of correct predictions / total items in fold `k`).

Compute the mean accuracy across the 3 folds for the current `T`.

**Step 2: Numerical Accuracy Logging**
Your script must log the cross-validation results to `/home/user/cv_results.txt`.
For each `T` in 2, 3, 4 (in that order), write a line formatted exactly as:
`T=[T], Accuracy=[Mean_Accuracy]`
The `Mean_Accuracy` must be formatted to exactly 4 decimal places (e.g., `T=2, Accuracy=0.8520`). Ensure strict numerical precision using `awk`.

**Step 3: Best Hyperparameter Selection**
Find the `T` that yielded the highest mean accuracy (in case of a tie, pick the smaller `T`). Write ONLY this single integer to `/home/user/best_t.txt`.

Constraints:
- You must write the solution in Bash (using `awk` is highly recommended for the math).
- The script `/home/user/clean_pipeline.sh` must be executable and runnable without arguments.
- Do not use Python, R, or Perl.