You are a Data Scientist tasked with building a reproducible anomaly detection pipeline in Rust to clean a noisy mathematical dataset.

We have two timeseries-like datasets: 
- `/home/user/train.csv` (Columns: `id`, `value`, `is_anomaly`)
- `/home/user/test.csv` (Columns: `id`, `value`)

You must create a Rust application that performs cross-validation to tune a hyperparameter for a Median Absolute Deviation (MAD) based anomaly detector, logs the experiment results, and then cleans the test set.

Here are the requirements for your Rust pipeline:

1. **Algorithm Definition**:
   An anomaly is defined as any point where:
   `|value - Median| > k * MAD`
   - `Median` is the median of the `value` column.
   - `MAD` (Median Absolute Deviation) is the median of the absolute differences between each `value` and the `Median`.
   - `k` is the tuning hyperparameter.
   *(Note: For even-sized arrays, compute the median as the simple arithmetic mean of the two middle elements).*

2. **Cross-Validation & Hyperparameter Tuning**:
   - Perform 4-fold cross-validation on `train.csv`.
   - The folds must be split sequentially without shuffling (e.g., if there are 80 rows, Fold 0 is rows 0-19, Fold 1 is 20-39, etc. The rows are 0-indexed based on their order in the CSV, ignoring the header).
   - For each fold (which serves as the validation set):
     - Use the other 3 folds as the training set.
     - Compute the `Median` and `MAD` using ONLY the training set.
     - Evaluate the anomaly detection on the validation set for `k` values: `1.0, 1.5, 2.0, 2.5, 3.0`.
     - Calculate the F1-score of the anomaly detection on the validation set. (Treat `is_anomaly = 1` as the positive class. If Precision + Recall == 0, F1 = 0.0).

3. **Experiment Tracking**:
   - Log the results of every validation fold evaluation to `/home/user/cv_results.csv`.
   - The file must have the header `k,fold,f1_score` (where fold is `0, 1, 2, 3` and f1_score is formatted to 4 decimal places).

4. **Cleaning the Test Set**:
   - Determine the best `k` that yields the highest average F1-score across the 4 folds. (In case of a tie, pick the smaller `k`).
   - Recompute the `Median` and `MAD` using the ENTIRE `train.csv` dataset.
   - Apply the detector with the best `k`, the global `Median`, and global `MAD` to `/home/user/test.csv`.
   - Keep only the rows that are NOT anomalies.
   - Save the cleaned data to `/home/user/cleaned_test.csv` (Columns: `id`, `value`).

Initialize a Rust project at `/home/user/anomaly_cleaner`, write the code, manage any dependencies you need (like `csv` or `serde`), and run the pipeline to produce the required output files. Use standard bash commands to execute your Rust project.