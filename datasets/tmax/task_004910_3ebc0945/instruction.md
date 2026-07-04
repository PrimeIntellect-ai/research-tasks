You are a data analyst working on evaluating the performance of several machine learning models. You have been provided with a CSV file at `/home/user/data/benchmarks.csv` containing performance metrics.

The CSV has the following columns (with a header row):
`model_id,inference_time_ms,accuracy,cpu_utilization`

Your task is to write a Bash script at `/home/user/analyze.sh` that calculates the Pearson correlation coefficient between `inference_time_ms` (column 2) and `accuracy` (column 3). 

However, you must adhere to the following strict requirements:
1. **Filtering:** You must only include rows where the `cpu_utilization` (column 4) is strictly greater than `50.0`.
2. **Language Constraint:** You must perform the math and data processing using **only** Bash, `awk`, and standard GNU Coreutils. Do not use Python, R, Perl, Ruby, or any other scripting languages, even if they are installed.
3. **Output:** The script must take the CSV file path as its first argument (e.g., `./analyze.sh /home/user/data/benchmarks.csv`). It should output a single number: the Pearson correlation coefficient rounded to exactly 4 decimal places.

Once you have written and tested your script, run it on the provided dataset and save the output to `/home/user/result.txt`.

Ensure your script handles the CSV header correctly and avoids division by zero.