You are a data scientist working with a massive stream of incoming IoT sensor data. Sometimes, the data pipeline receives corrupted files due to sensor resets or network retries. 

Your objective is to create a robust Bash classifier script at `/home/user/detect.sh` that evaluates a given CSV file and determines if it is "clean" or "anomalous". The script must accept a single file path as an argument. It must exit with code `0` if the file is clean, and exit with code `1` if the file is anomalous.

A CSV file (format: `timestamp,sensor_id,value`) is considered anomalous if it meets EITHER of the following criteria:
1. **Changepoint Anomaly:** For any given `sensor_id`, if the `value` drops by 50% or more strictly between two chronologically consecutive readings (based on `timestamp`).
2. **Duplication Anomaly:** If the file contains duplicate payload data. A payload is defined by the normalized combination of `sensor_id` and `value`. To check for duplication, you MUST use the vendored utility `sh-hash-row` provided in the `libsh-data` package. If any two rows in the file produce the exact same payload hash, the file is anomalous.

**Vendored Package Requirements:**
We have provided a vendored shell utility package at `/app/libsh-data-1.2.0`. This package contains the `sh-hash-row` command which handles complex normalization and hash-based deduplication signatures. 
However, the package is currently slightly broken due to a configuration bug introduced by the upstream maintainers. You will need to inspect the package, fix the bug so that it correctly executes, and then utilize its `bin/sh-hash-row` executable in your pipeline. (Note: You do not have root access, so do not try to install it system-wide; invoke it or fix it in-place).

**Constraints:**
- Your classifier `/home/user/detect.sh` must be written entirely in Bash (using shell built-ins, coreutils like `awk`, `sort`, `sed`, etc.).
- Ensure your script correctly orchestrates the multi-stage pipeline: filtering/sorting by sensor, calculating moving differences to detect the 50% drop changepoint, and hashing payloads to detect duplicates.