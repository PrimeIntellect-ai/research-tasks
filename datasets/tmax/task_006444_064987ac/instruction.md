You are a Machine Learning Engineer restricted to a bare-bones Linux server without Python, R, or any high-level data science libraries. You must prepare a training dataset and calculate confidence intervals using only standard Bash tools (e.g., `awk`, `bc`, `shuf`, `sort`, `sed`).

You have been provided a dataset at `/home/user/sensor_data.csv` with the header: `id,v1,v2`.

Your objective is to write and execute a Bash script (save it as `/home/user/prepare_data.sh`) that performs feature engineering and bootstrap hypothesis testing:

1. **Feature Engineering**: 
   - Parse `/home/user/sensor_data.csv`.
   - Find the maximum value of the `v1` column.
   - Create a new file `/home/user/engineered.csv` with the header `id,v1,v2,v1_norm,v_diff`.
   - For every data row, compute `v1_norm` as `v1 / max(v1)` and `v_diff` as `v2 - v1`. 
   - Round both new columns to exactly 4 decimal places.

2. **Bootstrap Sampling**:
   - Using the data rows of `/home/user/engineered.csv` (excluding the header), generate 100 independent bootstrap samples. 
   - Each bootstrap sample must consist of $N$ rows drawn **with replacement**, where $N$ is the total number of data rows in `engineered.csv`. Use `shuf -r -n <N>` to perform the sampling.
   - For each of the 100 bootstrap samples, calculate the arithmetic mean of the `v1_norm` column.
   - Append each calculated mean (formatted to 4 decimal places) to `/home/user/bootstrap_means.txt`. This file should end up with exactly 100 lines.

3. **Confidence Interval (Hypothesis Testing)**:
   - Sort the values in `/home/user/bootstrap_means.txt` numerically.
   - Extract the 3rd value (lower bound) and the 98th value (upper bound) to construct an empirical 95% confidence interval.
   - Save these two values (lower bound on the first line, upper bound on the second line) to `/home/user/confidence_interval.txt`.

Ensure your script is executable and run it so the output files (`engineered.csv`, `bootstrap_means.txt`, `confidence_interval.txt`) are generated.