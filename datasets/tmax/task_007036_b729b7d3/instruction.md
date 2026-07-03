You are a Machine Learning Engineer preparing training data and establishing a baseline model using pure Bash and POSIX utilities (like `awk`, `sed`, `grep`). 

You have been given a raw system metrics log file located at `/home/user/raw_metrics.csv`. The file has a header and the following columns:
`timestamp,cpu_percent,mem_percent,network_in_kb,network_out_kb,error_flag`

Your task is to build a bash-based ETL pipeline, run a lightweight baseline model inference, and benchmark it.

**Step 1: ETL Pipeline (`/home/user/run_etl.sh`)**
Write a bash script that processes `/home/user/raw_metrics.csv` and produces `/home/user/clean_features.csv`.
Rules for cleaning:
1. Ignore the header.
2. Filter out any rows where `error_flag` is `1` or where any column contains empty/missing values.
3. Extract only the feature columns: `cpu_percent`, `mem_percent`, `network_in_kb`, `network_out_kb`.
4. Convert the network columns from KB to MB (divide by 1024) and format to 2 decimal places.
5. The output `/home/user/clean_features.csv` must be a comma-separated file with NO header, in the order: `cpu,mem,net_in_mb,net_out_mb`.

**Step 2: Baseline Model Inference (`/home/user/run_inference.sh`)**
We have a baseline linear model to predict system overload. The weights are:
- `w_cpu = 0.6`
- `w_mem = 0.3`
- `w_net_in = 0.05`
- `w_net_out = 0.05`
- `bias = -65.0`

Write a bash script using `awk` or `bash` math that reads `/home/user/clean_features.csv`.
For each row, calculate the score: `score = (w_cpu * cpu) + (w_mem * mem) + (w_net_in * net_in_mb) + (w_net_out * net_out_mb) + bias`.
If `score > 0`, the prediction is `1` (overload), otherwise `0`.
Output the predictions (just the integers `0` or `1`, one per line) to `/home/user/predictions.txt`.

**Step 3: Validation & Reporting**
Create a summary report at `/home/user/report.txt` with exactly three lines:
Line 1: The total number of rows in `clean_features.csv`
Line 2: The total number of positive predictions (`1`s) in `predictions.txt`
Line 3: The string "Pipeline Complete"

Ensure all scripts are executable and run them to generate the final output files.