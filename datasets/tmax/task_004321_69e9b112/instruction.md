You are a log analyst investigating patterns in a multilingual server telemetry dataset. You have been given a raw, wide-format CSV log file containing Personally Identifiable Information (PII), multi-language event actions, and system metrics. 

Your objective is to build an ETL pipeline that anonymizes the data, reshapes it, normalizes the text, and calculates rolling statistics, saving the final output to `/home/user/clean_metrics.csv`.

**Data Source:**
File: `/home/user/server_logs.csv`
Columns: `Timestamp, UserID, UserName, Action, CPU_Usage, RAM_Usage, Disk_IO, Net_IO`

**Processing Requirements:**
1. **Data Masking & Anonymization:** 
   - Drop the `UserName` column completely.
   - Replace the `UserID` with an MD5 hash of the original `UserID`. Name this new column `UserHash`.

2. **Multilingual Text Normalization:**
   - The `Action` column contains event descriptions in multiple languages (English, Spanish, Mandarin, etc.).
   - A proprietary, stripped binary tool is provided at `/app/normalize_action`. It reads a raw action string from standard input (`stdin`) and prints the normalized string to standard output (`stdout`). 
   - You must pass every `Action` string through this binary to get the `NormalizedAction`. (Hint: You can call it as a black box or reverse-engineer its logic to implement it faster in your script).

3. **Wide-Long Format Reshaping:**
   - Reshape the 4 system metrics (`CPU_Usage`, `RAM_Usage`, `Disk_IO`, `Net_IO`) from wide format into long format.
   - You should have two new columns: `MetricName` (e.g., 'CPU_Usage') and `MetricValue` (the numerical value).

4. **Rolling Statistics:**
   - For each unique combination of `UserHash` and `MetricName`, sort the records chronologically by `Timestamp`.
   - Calculate a **3-period simple moving average** of the `MetricValue`. This means averaging the current value with up to 2 of the immediate previous values for that specific user and metric. 
   - If only 1 or 2 values are available (at the start of a user's sequence), average whatever is available. Round the final average to 2 decimal places. Name this column `RollingAvg`.

**Final Output Format:**
Write the processed data to `/home/user/clean_metrics.csv` with exactly the following columns, sorted ascending by `Timestamp`, then `UserHash`, then `MetricName`:
`Timestamp, UserHash, NormalizedAction, MetricName, RollingAvg`

**Evaluation:**
Your output will be graded programmatically. An evaluation script will compare your `/home/user/clean_metrics.csv` against a hidden ground-truth file. The metric calculated is the Row Accuracy Percentage (0 to 100). 
Your solution must achieve a score of **>= 98.0**.