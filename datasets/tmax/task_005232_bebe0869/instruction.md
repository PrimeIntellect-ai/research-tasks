You are a data engineer responsible for fixing and optimizing a legacy ETL pipeline. We receive daily telemetry data that is currently failing to process correctly due to data quality issues and slow execution. 

Your task is to write a robust Bash script at `/home/user/run_etl.sh` that processes a messy dataset and feeds it into a proprietary encoding binary.

**Input Data:**
- File: `/home/user/data/raw_telemetry.csv`
- Format: `timestamp,device_id,metric_val,log_msg` (with a header row)
- **Known Issues:** 
  1. The `log_msg` field is enclosed in double quotes but often contains **embedded newlines**. Our downstream binary silently drops rows if it encounters unexpected line breaks.
  2. The `metric_val` column frequently has missing values (empty strings like `,,`).

**The Processor Binary:**
- Location: `/app/telemetry_encoder`
- This is a compiled, stripped proprietary binary. It reads exactly 4 comma-separated fields from standard input (`timestamp,device_id,metric_val,log_msg`) and outputs `fingerprint_hash,encoded_vector` for each valid line.

**Pipeline Requirements:**
1. **Normalization:** Parse the CSV and replace any embedded newlines inside the quoted `log_msg` fields with a single space, ensuring each record strictly occupies a single line.
2. **Imputation:** For missing `metric_val` entries, perform a forward-fill (carry forward the last observed `metric_val` for that specific `device_id`). If it is the first reading for a device and it is missing, default to `0.0`.
3. **Tokenization:** Convert the `log_msg` strings to lowercase and replace all non-alphanumeric characters (excluding spaces) with spaces.
4. **Parallel Processing:** Pass the cleaned rows to `/app/telemetry_encoder`. The binary processes lines slowly. You **must** parallelize the data ingestion into the binary (e.g., using `xargs -P 4` or `parallel`) to speed up execution.
5. **Deduplication:** The pipeline must deduplicate the binary's output based on the `fingerprint_hash` (the first column of the binary's output). Keep only the first occurrence of each fingerprint.
6. **Output:** Write the final deduplicated data to `/home/user/final_output.csv`.

Your solution must be written primarily in Bash (using standard Linux utilities like `awk`, `sed`, `grep`, `xargs`, etc.). Python/Perl should not be used as the primary driver, though small inline snippets are permitted if strictly necessary for CSV parsing.

Make sure `/home/user/run_etl.sh` is executable and can be run without any arguments.