You are tasked with porting a system metrics processing tool so it can run inside a minimal, highly restricted Linux container. The current system relies on heavy third-party libraries (like pandas and numpy), which cannot be installed in the new container environment. You must write a pure Python 3 standard library solution.

The legacy system stored data in a flat CSV file located at `/home/user/legacy_metrics.csv`. 
Your goal is to write a script at `/home/user/metric_porter.py` that processes this CSV and performs a schema migration to a new nested JSON format, while applying a rolling numerical algorithm using a custom data structure.

Requirements:
1. **Custom Data Structure**: Implement a `TimeSeriesRingBuffer` class from scratch to store the sliding window of CPU metrics. It must strictly maintain a maximum size of `W=3` (evicting the oldest entries when full).
2. **Numerical Algorithm**: As you process each row chronologically, calculate the Simple Moving Average (SMA) and the Population Variance for the `cpu_util` metric over the rolling window of size 3. 
   - If there are fewer than 3 elements (i.e., the first two rows), calculate the SMA and Variance using only the available elements.
   - Population variance formula: `sum((x - SMA)^2 for x in window) / len(window)`.
   - Do NOT use the `statistics` module's variance functions. Implement it manually to ensure population variance (divide by N, not N-1) is used.
3. **Schema Migration**: Transform the flat CSV schema into a specific nested JSON structure. 
   - Old Schema (CSV): `timestamp` (int), `cpu_util` (float), `memory_util` (float)
   - New Schema (JSON): An array of objects. Each object must have:
     - `ts`: integer (mapped from `timestamp`)
     - `metrics`: an object containing `cpu` (float) and `mem` (float)
     - `stats`: an object containing `cpu_sma_3` (float) and `cpu_var_3` (float)
4. **Formatting**: Round all floating-point numbers in the output JSON to exactly 4 decimal places.
5. **Output**: Save the resulting JSON array to `/home/user/migrated_metrics.json`.

Write and execute `/home/user/metric_porter.py` to generate the output file. Ensure no third-party libraries are imported.