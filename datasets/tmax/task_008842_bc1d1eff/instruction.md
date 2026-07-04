You are a log analyst investigating coordinated anomalies across multiple sensors in a time-series dataset. 

You have been provided with a dataset of sensor readings at `/home/user/sensor_data.txt`. The file contains three space-separated columns: `SensorID`, `Timestamp`, and `Value`. The rows are not guaranteed to be sorted.

Your task is to identify which sensors exhibit the exact same "shape" of behavior over time, and generate a report. The "shape" of a sensor's time series is defined as the sequence of differences (deltas) between consecutive values when ordered chronologically.

Perform the following steps using only Bash, standard coreutils, and tools like `awk` or `sed`:

1. **Calculate Deltas**: For each `SensorID`, sort its readings by `Timestamp` (ascending). Compute the difference between consecutive `Value`s (Current_Value - Previous_Value). 
2. **Hash-Based Deduplication**: Join these deltas into a comma-separated string (e.g., `5,-2,7`). Compute the MD5 hash of this exact string (ensure you do not include a trailing newline when hashing, i.e., use `echo -n` or `printf`). This hash represents the sensor's pattern signature.
3. **Pipeline Logging**: As your script calculates the hash for a sensor, it must append a line to `/home/user/pipeline.log` in the format: `Processed sensor: <SensorID>`.
4. **Identify Matches**: Find the two sensors that have the exact same pattern signature (MD5 hash). There will be exactly one pair of sensors that match and have at least 2 deltas.
5. **Template-Based Generation**: Generate a report file at `/home/user/report.md` with exactly the following format (replace the bracketed placeholders, list the matching sensors in alphabetical order):

```markdown
# Anomaly Report

The following sensors share an identical behavior pattern:
- [First_SensorID]
- [Second_SensorID]

Pattern Hash: [MD5_Hash]
```

Write and execute the shell commands/scripts required to accomplish this.