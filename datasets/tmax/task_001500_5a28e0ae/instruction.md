You are a data scientist cleaning a batch of noisy sensor datasets. Your Lead Scientist has dictated the specific statistical rules for data cleaning in an audio memo. 

Your task is to build a data pipeline tool in Go that implements these rules.

1. Listen to the audio memo located at `/app/dictation.wav`.
2. Write a Go program at `/home/user/cleaner.go` and compile it to `/home/user/cleaner`.
3. The program must accept exactly one command-line argument: the path to a JSONL file containing sensor readings. 
   Format of each line: `{"sensor_id": "string", "timestamp": int64, "signal": float64}`
4. Your Go program must perform the following data processing pipeline:
   - **Cleaning & Deduplication:** If multiple records exist with the same `sensor_id`, keep *only* the record with the highest `timestamp`.
   - **Summary Statistics:** Calculate the mean ($\mu$) and population standard deviation ($\sigma$) of the `signal` values across the *deduplicated* dataset.
   - **Filtering:** Apply the exact statistical threshold rule dictated in the audio memo to identify outliers based on their z-score.
   - **Logging:** Print the calculated statistics and the number of rejected outlier records to `stderr` in exactly this format:
     `STATS: mean=<val> stddev=<val> rejected=<count>` (format floats to 2 decimal places).
   - **Output:** Print the surviving (accepted), deduplicated JSONL records to `stdout` (one per line, order does not matter).

Your tool will be tested against a hidden corpus of files. It must perfectly preserve all valid data points while rejecting outliers and duplicates according to the dictated rule.