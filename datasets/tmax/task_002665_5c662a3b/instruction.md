You are a data engineer responsible for building a robust Bash-based ETL pipeline to process incoming IoT time-series data. 

We have received an image containing the configuration parameters for our anonymization pipeline. The image is located at `/app/salt.png`.

Your task is to write an ETL shell script at `/home/user/etl.sh` that processes CSV data from Standard Input (stdin) and outputs JSON Lines to Standard Output (stdout).

### Requirements for `/home/user/etl.sh`:
1. **Input Format**: The script will read CSV data from stdin. The first line is always the header: `ts,dev,val`. 
   - `ts`: Integer Unix timestamp.
   - `dev`: String device identifier (e.g., `deviceA`).
   - `val`: Float value (e.g., `12.5`). Sometimes this field is empty, representing a missing reading.
   - The input lines are NOT guaranteed to be sorted by timestamp.

2. **Interpolation/Imputation**: 
   - Sort the records chronologically by timestamp.
   - For each device independently, forward-fill any missing `val` fields (use the most recent chronologically preceding value for that specific device). 
   - If a device's first chronologically sorted reading is missing a value, impute it as `0.0`.

3. **Aggregation**:
   - Group the data into 1-hour tumbling windows (3600 seconds). A window starts at `int(ts / 3600) * 3600`.
   - Calculate the maximum value (`max_val`) for each device within each window.

4. **Data Masking**:
   - Extract the masking salt from the image `/app/salt.png`. The image contains text like `MASK_SALT: <SALT_STRING>`. You must use OCR (e.g., `tesseract`) to read it.
   - Anonymize the `dev` string by concatenating the device name and the salt (e.g., if dev is `deviceA` and salt is `XYZ`, the string is `deviceAXYZ`).
   - Compute the MD5 hash of this concatenated string (do not include newlines in the hash input).
   - The masked device ID is the first 8 characters of the resulting MD5 hex hash.

5. **Output Format**:
   - Output one JSON object per line (JSONL format).
   - Format: `{"window": 1600000000, "device": "abcdef12", "max_val": 15.2}`
   - Format `max_val` to 1 decimal place.
   - Sort the final output first by `window` (ascending), then by the anonymized `device` string (ascending).

6. **Pipeline Scheduling**:
   - Create a file at `/home/user/cron.txt` containing a valid cron expression to schedule `/home/user/etl.sh` to run every 15 minutes, redirecting input from `/data/in.csv` and output to `/data/out.jsonl`.

Ensure your script `/home/user/etl.sh` is executable and strictly uses Bash, standard coreutils (awk, sort, md5sum, etc.).