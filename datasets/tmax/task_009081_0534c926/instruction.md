You are a data engineer working on a high-performance ETL pipeline. We have a stream of telemetry data in JSON-lines format, but the system generating it has a bug: it sometimes outputs malformed unicode escape sequences (e.g., `\uXYZW` instead of valid hex digits). Standard JSON parsers break on these lines.

Your task is to write a C program that cleans this data, parses it, joins it with a CSV metadata file, and performs time-series resampling and gap-filling.

**Input Files:**
1. `/home/user/telemetry.jsonl`
   A JSON-lines file where each line is a JSON object like:
   `{"ts": 1700000000, "sensor": "S1", "val": 10.5, "msg": "status \uZZZZ"}`
   - `ts`: Integer Unix timestamp.
   - `sensor`: String identifier.
   - `val`: Float reading.
   - `msg`: String that may contain malformed unicode escapes.

2. `/home/user/metadata.csv`
   A CSV file with headers: `sensor_id,location,group`

**Requirements for your C program (`/home/user/process.c`):**

1. **Clean the JSON:**
   Read `telemetry.jsonl` line by line. Before parsing the JSON, you must sanitize the `msg` field.
   Find any occurrence of `\u` followed by exactly 4 characters. If ANY of those 4 characters is NOT a valid hexadecimal digit (`0-9`, `a-f`, `A-F`), replace the entire 6-character sequence (the `\u` and the 4 bad characters) with the string `[ERR]` (which is 5 characters long, so you will need to shift the rest of the string). 

2. **Parse and Join:**
   Parse the cleaned JSON (you may download a lightweight library like `cJSON` via `wget` or `curl`, or parse the flat string manually since the structure is highly predictable). 
   Join the telemetry data with `metadata.csv` using `sensor` == `sensor_id`.

3. **Resample and Gap-Fill:**
   We need the output to have strictly 10-second intervals for *each* sensor found in the metadata file, starting from `ts = 1700000000` to `ts = 1700000050` inclusive.
   - If a sensor has a reading at a specific 10-second timestamp, use that `val`.
   - If a timestamp is missing for a sensor, **forward-fill** using the `val` from the previous timestamp for that sensor.
   - If there is no previous reading for a sensor (e.g., at `1700000000`), use `0.0`.

4. **Output:**
   Write the final transformed data to `/home/user/output.csv` with the exact following header and comma-separated format:
   `ts,sensor_id,location,val`
   Sort the output primarily by `sensor_id` (alphabetically) and secondarily by `ts` (ascending). Format `val` to exactly 1 decimal place (e.g., `10.5`).

Compile your program using `gcc /home/user/process.c -o /home/user/process` (and any necessary flags like `-lm`) and execute it to generate the `output.csv`.