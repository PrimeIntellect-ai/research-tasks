You are tasked with building a data processing script to track configuration changes across our microservices. Our configuration manager emits logs whenever a service's memory limit is updated. Due to network delays and retries, these logs often contain exact duplicates and are asynchronous. 

You need to write a Python script that processes these raw configuration logs into a clean, minute-by-minute time-series report.

**Input Data:**
There are two CSV files located at:
1. `/home/user/configs/svc_alpha.csv`
2. `/home/user/configs/svc_beta.csv`

Each CSV has the following columns: `timestamp`, `param_name`, `param_value`.
Example row: `2023-10-01 10:00:15, memory_mb, 512`

**Processing Requirements:**
1. **Cleaning:** Remove exact duplicate rows (same timestamp, param, and value) within each file.
2. **Resampling & Gap-Filling:** Create a strict minute-by-minute timeline starting exactly at `2023-10-01 10:00:00` and ending at `2023-10-01 10:10:00` (inclusive). For each minute `T`, determine the active memory configuration for each service. The active configuration is the value of the *most recent* change that occurred at or before `T`. If a service has no configuration changes at or before `T`, its active memory is `0`.
3. **Merging:** Combine the active configurations of both `alpha` and `beta` services to compute the `total_memory` allocated across both services for each minute.
4. **Rolling Statistics:** Calculate a 3-minute rolling average of the `total_memory` (i.e., the average of the current minute and the previous 2 minutes). For the first two minutes, compute the average using only the available data points (e.g., at 10:01:00, use 10:00:00 and 10:01:00). Round this rolling average to exactly 2 decimal places.

**Output Specification:**
Save the final time-series data as a JSON file at `/home/user/memory_report.json`.
The JSON should be an array of objects, ordered chronologically. Each object must have exactly these keys and formats:
- `"timestamp"`: string (Format: `"YYYY-MM-DD HH:MM:SS"`)
- `"total_memory"`: integer
- `"rolling_avg"`: float (rounded to 2 decimal places)

Example structure:
```json
[
  {
    "timestamp": "2023-10-01 10:00:00",
    "total_memory": 0,
    "rolling_avg": 0.0
  },
  ...
]
```

Use any Python libraries you need (e.g., pandas). You may install dependencies if they are missing. Create your script and execute it to generate the final JSON file.