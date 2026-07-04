You are a data analyst troubleshooting an ETL pipeline. An automated ETL job failed and retried several times last night, resulting in multiple fragmented and overlapping CSV exports in `/home/user/data/`.

Your task is to write a Bash script at `/home/user/process_data.sh` that cleans, deduplicates, and aggregates this data using only standard Linux command-line tools (e.g., `awk`, `sort`, `grep`, `sed`, `bash`). Python, Perl, or other high-level scripting languages are strictly forbidden.

The input directory `/home/user/data/` contains three files:
- `export_A.csv`
- `export_B.csv`
- `export_retry.csv`

All files have the same header: `tx_id,user_id,amount,timestamp,retry_flag`

Your script must perform the following pipeline and output the final result to `/home/user/output/clean_rolling_tx.csv`.

**Phase 1: Union & Constraint Validation**
Combine all three files (ignoring all but one header). Filter out invalid rows based on these constraints:
1. `amount` must be strictly greater than 0.
2. `tx_id` must be strictly alphanumeric (letters and numbers only, no hyphens, underscores, or spaces).

**Phase 2: Deduplication**
Due to the ETL retries, the same `tx_id` may appear multiple times across or within the files. 
For any duplicate `tx_id`, you must keep exactly one record: the one with the highest `timestamp`. If there is a tie on `timestamp`, keep the one with the highest `retry_flag` value.

**Phase 3: Windowed Aggregation**
Using the cleaned and deduplicated data, calculate a 2-transaction rolling sum of the `amount` for each `user_id`, ordered by `timestamp` ascending.
- The rolling sum for a transaction is the `amount` of that transaction plus the `amount` of the strictly previous transaction for that SAME `user_id` (if one exists).

**Output Format**
The final output file `/home/user/output/clean_rolling_tx.csv` must be a CSV with exactly this header:
`tx_id,user_id,amount,rolling_sum`
The rows must be sorted ascending by `user_id`, and then ascending by `timestamp`.

Ensure your script `/home/user/process_data.sh` is executable and creates the output directory if it doesn't exist.