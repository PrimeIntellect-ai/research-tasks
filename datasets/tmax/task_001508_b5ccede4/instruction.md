You are a log analyst investigating an upstream ETL job that has been misbehaving. The job has been sending server metric logs (CPU and Memory) over a flaky network. Due to retries, there are duplicate records, out-of-order logs, and gaps in the time series. Additionally, some corrupted logs contain impossible values.

You need to write a C program that cleans, deduplicates, and resamples this time-series data. 

**Requirements:**
Write a C program at `/home/user/process_metrics.c` that accepts two command-line arguments: the input CSV file path and the output CSV file path.
`./processor /home/user/raw_metrics.csv /home/user/clean_metrics.csv`

**Data Processing Rules:**
1. **Input Format**: A CSV file with a header `timestamp,cpu_usage,memory_mb`. Timestamps are Unix epoch integers. CPU usage and memory are integers. The lines can be in any order.
2. **Validation**: Drop any row where `cpu_usage < 0` or `cpu_usage > 100`. Drop any row where `memory_mb < 0`.
3. **Deduplication**: If multiple valid rows share the same `timestamp`, keep the one with the maximum `cpu_usage`. If there is a tie in CPU usage, keep the one with the maximum `memory_mb`.
4. **Resampling and Gap-Filling**: Generate a continuous time series at exactly 1-second intervals from the minimum valid timestamp to the maximum valid timestamp.
    *   If a timestamp has a valid record, use it.
    *   If a timestamp is missing, use **forward-fill** (copy the values from the previous second) if the gap (number of missing seconds between valid records) is **5 seconds or fewer**.
    *   If the gap between valid records is **strictly greater than 5 seconds**, insert `-1` for both `cpu_usage` and `memory_mb` for all missing seconds in that gap.
5. **Output Format**: Write the results to the output file with the header `timestamp,cpu_usage,memory_mb`, sorted chronologically by timestamp ascending.

Compile your program into an executable named `/home/user/processor` using `gcc` and run it against the provided `/home/user/raw_metrics.csv` file. 
Ensure the cleaned data is written to `/home/user/clean_metrics.csv`.