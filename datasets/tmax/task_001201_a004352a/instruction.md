**[PagerDuty Alert - 03:14 AM]**
**Service:** `telemetry-anomaly-detector`
**Severity:** CRITICAL
**Description:** The anomaly detection pipeline is failing. The variance calculations are returning wildly negative numbers (which is mathematically impossible), and the logs show data from unknown Sensor IDs. 

You are the on-call engineer. The failing service is driven by a script located at `/home/user/anomaly_detector.py`. It reads a base64-encoded binary telemetry stream from `/home/user/telemetry.b64`.

The stream is supposed to contain a sequence of records. Each record consists of:
1. A Sensor ID (32-bit signed integer, little-endian)
2. A sensor reading (64-bit double-precision floating point, little-endian)

Recent changes to the upstream data serialization or the local parsing code have broken the pipeline. Your tasks:
1. Identify and fix the serialization/encoding mismatch that is causing the parser to read garbage Sensor IDs and misaligned data.
2. Identify why the floating-point variance calculation is producing negative numbers (catastrophic cancellation) and replace it with a numerically stable method (calculate the **population** variance).
3. Process the data in `/home/user/telemetry.b64` successfully.
4. Write the corrected population variance for each valid Sensor ID to `/home/user/fixed_variances.txt`.

**Output Format Requirements for `/home/user/fixed_variances.txt`:**
Each line should be exactly in the format `SensorID: Variance`.
Round the variance to exactly 4 decimal places. Sort the output by Sensor ID in ascending order.
Example:
```
1: 0.0200
2: 0.1067
```

Fix the script, run it, and generate the required output file. You may rewrite the script in any language of your choice, provided the output is correct.