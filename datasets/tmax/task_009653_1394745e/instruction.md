You are a Data Analyst tasked with processing a dataset of server logs combining system metrics and text logs. Your goal is to prepare the dataset, clean the data, extract text features, and perform statistical analysis to understand the impact of specific events on system latency.

The raw dataset is located at: `/home/user/server_logs.csv`

Please perform the following steps and save your results to a JSON file at `/home/user/analysis_report.json`.

**Step 1: Environment Configuration**
Before running your analysis script, ensure that your numerical libraries are constrained to a single thread to simulate a restricted processing environment. You must configure the environment variables `OMP_NUM_THREADS` and `OPENBLAS_NUM_THREADS` to `1` in your shell before running your Python script.

**Step 2: Data Cleaning (Missing Values and Outliers)**
1. Load the CSV. It has the following columns: `timestamp`, `cpu_usage`, `memory_usage`, `latency_ms`, and `log_message`.
2. **Missing Values**: Calculate the median of the `latency_ms` column (ignoring NaNs). Fill any missing (`NaN`) values in `latency_ms` with this median.
3. **Outliers**: Calculate the sample mean and sample standard deviation (`ddof=1`) of the `cpu_usage` column. Identify outliers as any value strictly greater than `mean + 3 * std` or strictly less than `mean - 3 * std`. Cap these outliers to the exact `mean + 3 * std` or `mean - 3 * std` boundaries respectively. Count how many rows were capped.

**Step 3: Text Tokenization and Dataset Preparation**
1. Process the `log_message` column to extract a vocabulary.
2. For each message: Convert to lowercase, remove all characters that are not alphanumeric or whitespace (e.g., remove punctuation), and split into tokens by whitespace.
3. Calculate the total vocabulary size (number of unique tokens across the entire dataset).

**Step 4: Hypothesis Testing and Confidence Intervals**
We want to test if the presence of the word "timeout" in the tokenized log messages is associated with higher latency.
1. Divide the dataset into two groups based on the tokenized `log_message`: 
   - Group A: Rows where the exact token `"timeout"` is present.
   - Group B: Rows where the exact token `"timeout"` is NOT present.
2. Using the imputed `latency_ms` data, perform an independent two-sample Welch's t-test (unequal variances) to compare the means of Group A and Group B. (Alternative hypothesis: two-sided).
3. Calculate the 95% Confidence Interval for the difference in means (`mean(Group A) - mean(Group B)`). You may use `scipy.stats` for the t-distribution critical value (using Welch-Satterthwaite degrees of freedom, or simply using `scipy.stats.ttest_ind` which can provide confidence intervals in recent Scipy versions. If computing manually, use the standard Welch's CI formula).

**Output Format**
Write a JSON file to `/home/user/analysis_report.json` with exactly the following keys:
- `"median_latency_imputed"`: The median value used to fill missing latencies (float, round to 4 decimal places).
- `"cpu_outliers_capped"`: The number of `cpu_usage` rows that were capped (integer).
- `"vocab_size"`: The total number of unique tokens across all messages (integer).
- `"t_stat"`: The calculated t-statistic (float, round to 4 decimal places).
- `"p_value"`: The calculated p-value (float, round to 4 decimal places).
- `"ci_lower"`: The lower bound of the 95% CI for the difference in means (float, round to 4 decimal places).
- `"ci_upper"`: The upper bound of the 95% CI for the difference in means (float, round to 4 decimal places).