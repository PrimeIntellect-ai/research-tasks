You are a Machine Learning Engineer preparing training data for a web application firewall (WAF) anomaly detection model. Your task is to process raw web server logs to extract features, tokenize URLs, and track dataset generation metrics.

You must write a Bash script located at `/home/user/prepare_data.sh` that takes exactly one argument: an `EXPERIMENT_ID` (e.g., `exp_001`). 

The script must process the raw log file located at `/home/user/raw_access.log`. The log format is a simplified common log format:
`IP - - [Date] "METHOD URL PROTOCOL" STATUS SIZE`

Your script must perform the following data preparation and feature engineering steps for each line in the log file, and output the results to `/home/user/dataset_<EXPERIMENT_ID>.csv`.

**Data Preparation & Feature Engineering:**
1. Extract the `METHOD` (e.g., GET, POST), the `URL` path + query string, and the HTTP `STATUS` code.
2. **Feature 1 (`url_len`):** Calculate the integer character length of the exact extracted `URL`.
3. **Feature 2 (`param_count`):** Count the number of equals signs (`=`) in the `URL`.
4. **Feature 3 (`suspicious`):** A binary flag (`1` or `0`). Set to `1` if the `URL` contains any of the following substrings (case-insensitive): `eval`, `base64`, or `script`. Otherwise, `0`.
5. **Tokenization (`tokenized_url`):** Replace all non-alphanumeric characters (anything that is not `a-z`, `A-Z`, or `0-9`) in the `URL` with a single space. Squeeze multiple consecutive spaces into a single space, and trim leading/trailing spaces. Convert the final string to lowercase.

**Output Dataset Format:**
Create `/home/user/dataset_<EXPERIMENT_ID>.csv` with a header line exactly as follows:
`method,status,url_len,param_count,suspicious,tokenized_url`
Following the header, append the engineered features for each log line in the exact same order, comma-separated.

**Experiment Tracking:**
After creating the dataset, the script must append a single tracking record to `/home/user/experiment_log.csv`.
If the file does not exist, create it and include this header:
`experiment_id,total_rows,suspicious_count`
Append a new line containing the `EXPERIMENT_ID`, the total number of processed log lines (excluding headers), and the total count of rows where the `suspicious` flag was `1`.

**Execution:**
Once you have written the script, ensure it is executable and run it once with the experiment ID `run_baseline`.