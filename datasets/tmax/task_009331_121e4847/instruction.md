You are a Data Engineer building a lightweight, dependency-free ETL and analytics pipeline that must run entirely using standard Linux utilities (Bash, Awk, Sed, etc.) without relying on Python, R, or any external binaries not found in a standard GNU coreutils environment. 

We have a dataset of user events at `/home/user/events.csv` with the following header:
`id,category,value,label`
Where:
- `id`: Row identifier (integer, 1-indexed, starting after the header)
- `category`: Categorical feature (A, B, or C)
- `value`: Numeric measurement (integer)
- `label`: Binary target (0 or 1)

Write a single Bash script at `/home/user/etl_pipeline.sh` that performs the following three phases. The script must execute without errors when run as `bash /home/user/etl_pipeline.sh`.

**Phase 1: Tabular Aggregation**
Compute the average `value` for each `category`. 
- Output the result to `/home/user/phase1_aggregates.csv`.
- Format: `category,average_value` (include this header).
- Sort the rows alphabetically by `category`.
- Round the average to exactly 2 decimal places (e.g., `45.67`).

**Phase 2: Bootstrap Confidence Interval**
We want to estimate the mean of `value` across the entire dataset using bootstrapping.
To ensure deterministic evaluation, we have provided a file containing pre-generated bootstrap resampling indices at `/home/user/bootstrap_indices.txt`.
- The file has exactly 100 lines. Each line represents one bootstrap sample and contains exactly 1000 comma-separated row indices (ranging from 1 to the total number of data rows).
- For each of the 100 lines, extract the `value` for the corresponding row indices from `events.csv`, and calculate the mean `value` of that sample (round to 2 decimal places).
- Sort these 100 sample means in ascending order.
- Find the 5th percentile (the 5th smallest value) and the 95th percentile (the 95th smallest value).
- Output these two values separated by a comma to `/home/user/phase2_ci.txt` (format: `p5_mean,p95_mean`). No newline at the end is strictly required, but no text other than the two numbers should be present.

**Phase 3: Cross-Validation & Bayesian Inference**
Implement a 5-fold cross-validated Naive Bayes classifier using strictly Bash/Awk to predict `label` based ONLY on `category`.
- Assign each data row (excluding header) to a fold (0 through 4) using `(row_number - 1) % 5`. For example, row 1 is fold 0, row 2 is fold 1... row 5 is fold 4, row 6 is fold 0.
- For each fold $i$ from 0 to 4, treat fold $i$ as the validation set and the other four folds as the training set.
- Using the training set, compute the prior probabilities $P(label=0)$ and $P(label=1)$.
- Compute the conditional likelihoods $P(category=c | label=0)$ and $P(category=c | label=1)$ for all categories.
- For each row in the validation set, predict the label that maximizes $P(label) \times P(category | label)$. If the probabilities are exactly equal, default to predicting `1`.
- Calculate the overall accuracy across all 5 folds (Total Correct Predictions / Total Rows).
- Output the overall accuracy rounded to 4 decimal places to `/home/user/phase3_accuracy.txt`.

Ensure your script is self-contained, executable, and relies only on POSIX-compliant shell features or standard GNU utilities (e.g., `awk`, `grep`, `sort`, `bc`).