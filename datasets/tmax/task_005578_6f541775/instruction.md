You are a data analyst at a software company analyzing customer feedback. You have been provided with a CSV file at `/home/user/customer_data.csv` containing the following columns: `user_id`, `feedback_text`, `interaction_time`, and `is_premium`.

Your goal is to prepare this dataset, extract token-based features, perform statistical analysis, and store the resulting data in an optimized format for large-scale querying.

Please perform the following steps:
1. **Tokenization & Dataset Preparation:**
   - Read `/home/user/customer_data.csv`.
   - Create a new column called `token_count`. To calculate this, process `feedback_text` by:
     - Converting the text to lowercase.
     - Removing all non-alphanumeric characters (excluding spaces).
     - Splitting the text by spaces.
     - Removing any empty string tokens.
     - Counting the number of resulting tokens.

2. **Correlation Analysis:**
   - Calculate the Pearson correlation coefficient between `token_count` and `interaction_time`.

3. **Hypothesis Testing:**
   - We want to know if premium users write significantly different amounts of feedback compared to non-premium users.
   - Perform an independent two-sample t-test (Welch's t-test, assuming unequal variances) comparing the `token_count` of premium users (`is_premium == 1`) against non-premium users (`is_premium == 0`).

4. **Large-scale Data Storage Management:**
   - Save the fully processed dataframe (including the new `token_count` column) to a Parquet file at `/home/user/processed_data.parquet` using `snappy` compression.

5. **Reporting:**
   - Create a JSON file at `/home/user/stats_report.json` containing the results of your statistical tests.
   - The JSON should have the exact following structure, with floats rounded to 4 decimal places:
     ```json
     {
       "correlation": <pearson_correlation_coefficient>,
       "t_stat": <welchs_t_statistic>,
       "p_value": <welchs_p_value>
     }
     ```