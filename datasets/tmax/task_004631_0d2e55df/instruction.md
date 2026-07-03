You are a data scientist tasked with building a robust data cleaning and anomaly detection pipeline for a continuous stream of IoT sensor data. 

We have a vendored Python package located at `/app/lib_dataclean` which provides utilities for data stream processing. However, the package contains a deliberate bug in its deduplication logic that you must identify and fix before using it.

Your objective is to:
1. Identify and fix the bug in `/app/lib_dataclean` (specifically in how it handles deduplication of consecutive identical rows).
2. Install the fixed package in your environment.
3. Write a Python script at `/home/user/process.py` that reads a CSV stream from `stdin` and writes the processed output to `stdout`.

The input stream on `stdin` will consist of headerless CSV lines in the format:
`timestamp,device_id,reading`

Your script must perform the following operations in order:
1. **Cleaning:** Discard any row where `reading` is not a valid integer.
2. **Deduplication:** Using the fixed `lib_dataclean.cleaner.Deduplicator`, discard consecutive rows that are strictly identical (all three fields match the immediately preceding emitted row).
3. **Rolling Statistics & Anomaly Detection:** Maintain a rolling window of the last 5 valid, non-duplicate `reading` values for each `device_id`. If a new reading causes the sum of the current window (up to 5 elements) to be **greater than or equal to 100**, this is flagged as an anomaly.
4. **Join:** For every anomaly detected, look up the `device_id` in the JSON file `/app/device_map.json` (format: `{"device_id": "location_name", ...}`). If the device is not found, use the string `"UNKNOWN"`.
5. **Output:** Print the anomaly to `stdout` as a CSV line in the exact format:
`timestamp,device_id,location_name,rolling_sum`

The automated test will evaluate your script by continuously piping thousands of fuzzed input lines into your script and comparing your `stdout` bit-for-bit against a highly optimized reference implementation. 

Ensure your script is executable (`chmod +x /home/user/process.py`) and includes the appropriate shebang (e.g., `#!/usr/bin/env python3`).