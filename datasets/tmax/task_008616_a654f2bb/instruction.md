You are a support engineer investigating an issue in a data processing pipeline. 

A Python script `/home/user/pipeline/process_data.py` calculates the average temperature from sensor data logs. Recently, downstream tests have started failing intermittently depending on the specific data file provided. You have been given a dataset `/home/user/sensor_data.csv` that consistently reproduces a crash.

The repository is located at `/home/user/pipeline`. The tag `v1.0` is known to be good, while `HEAD` is currently failing. 

Your task is to:
1. Use git bisection between `v1.0` and `HEAD` to find the exact commit hash that introduced the format parsing bug.
2. Trace the execution on the provided `/home/user/sensor_data.csv` to identify the exact 1-based line number in the CSV file that triggers the edge-case crash (a parsing failure due to anomalous data).
3. Generate a diagnostic report at `/home/user/diagnostic_report.txt` containing exactly two lines in the following format:

```
Bad Commit: <full_40_character_commit_hash>
Failing Line Number: <integer_line_number>
```

Do not include any other text in the `diagnostic_report.txt` file. Make sure you use the full 40-character commit hash of the first bad commit.