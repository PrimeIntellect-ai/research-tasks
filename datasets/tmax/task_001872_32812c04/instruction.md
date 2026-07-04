You are an MLOps engineer tracking model experiment artifacts. We have aggregated raw metrics from various training runs into a single CSV file, but the data is messy. 

Your task is to use standard Linux CLI tools (Bash, awk, grep, shuf, etc.) to clean the data, sample it, and evaluate a subset of the models.

The raw data is located at `/home/user/artifacts.csv`. The expected columns are: `run_id,accuracy,loss,latency_ms`.

Please perform the following steps:
1. **Schema Enforcement**: Filter the file to extract only valid records. A valid record must have exactly 4 comma-separated fields. The `run_id` (column 1) can be any string. `accuracy` (column 2), `loss` (column 3), and `latency_ms` (column 4) must be strictly numeric (digits and optionally a single decimal point). Discard any headers, empty lines, or malformed rows (e.g., those containing "N/A" or missing fields).
2. **Sampling**: From the valid records, extract a random sample of exactly 30 rows. To ensure reproducibility for this evaluation, you MUST use `shuf -n 30 --random-source=/home/user/random_seed` on the filtered data.
3. **Model Evaluation & Statistics**: Using your 30 sampled rows, calculate the mean `accuracy` and mean `loss`. 
4. **Reporting**: Write the final calculated means to `/home/user/evaluation_summary.txt` in exactly this format (rounded to exactly 4 decimal places):
   `Mean Accuracy: 0.XXXX, Mean Loss: 0.XXXX`

Do not write any other text to the output file. You should execute these steps entirely in the terminal.