You are a data analyst tasked with processing server performance metrics and text-based system logs to create an aligned, gap-filled summary dataset.

You have two input files located in your home directory:
1. `/home/user/metrics.csv`: Contains high-frequency, irregularly sampled server metrics in a wide format.
2. `/home/user/logs.csv`: Contains unstructured system log messages with irregular timestamps.

Your goal is to write a Python script that processes these files and produces a final summary CSV at `/home/user/summary.csv` meeting the following exact specifications:

**1. Metrics Processing (Wide-long reshaping, Resampling, and Gap-filling):**
- Read `/home/user/metrics.csv`.
- Reshape the data from wide format (with columns for `cpu`, `memory`, `disk`) into a long format with columns: `timestamp`, `metric`, `value`.
- Parse the timestamps (assumed UTC) and resample the data into strictly continuous 5-minute bins (e.g., 10:00:00 to 10:04:59 is labeled as 10:00:00).
- For each 5-minute bin and each metric, calculate the mathematical mean of the `value`.
- If a 5-minute bin has no data for a metric, forward-fill the mean value from the most recent available preceding bin.

**2. Log Processing (Tokenization and Normalization):**
- Read `/home/user/logs.csv`.
- Parse the timestamps (assumed UTC) and group them into the same 5-minute bins as the metrics.
- For the `message` field in each log, normalize the text: convert to lowercase, remove all punctuation (replace any character that is not alphanumeric or whitespace with an empty string), and tokenize by splitting on whitespace.
- Count the total combined occurrences of the exact target words `"error"` and `"timeout"` within each 5-minute bin. If a bin has no logs or no target words, the count should be `0`.

**3. Alignment and Output:**
- Merge the processed metrics and log counts based on the 5-minute timestamp bins.
- The final output file `/home/user/summary.csv` must contain exactly these columns in this order: `timestamp` (ISO 8601 format, e.g., `2023-10-01T10:00:00Z`), `metric` (the string name of the metric: cpu, memory, or disk), `mean_value` (rounded to 2 decimal places), and `alert_count` (integer count of the target words).
- Sort the final CSV ascending by `timestamp` and then ascending by `metric` alphabetically.

Ensure your Python script runs successfully and creates the `/home/user/summary.csv` file before you finish the task.