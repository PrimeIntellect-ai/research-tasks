I am a researcher working with an array of environmental sensors, and I need help organizing my dataset. The data is currently scattered across a deeply nested directory structure under `/home/user/dataset_raw/`. 

The raw logs were saved using a custom compression and encoding format by a legacy system to save space. I need you to navigate the directory tree, find all these custom files, decompress them, filter for critical events, convert the format, and consolidate everything into a single CSV file.

Here is the precise specification for the task:

1. **Locate the files**: Find all files with the `.cst` (custom) extension inside `/home/user/dataset_raw/` and its subdirectories.
2. **Decompress and Decode**: Write a Python script to stream and decode these files. The custom `.cst` format works as follows:
   - Each line represents a compressed record in the format `<repeat_count>:<base64_encoded_string>`.
   - You must read each line, decode the base64 string, and then duplicate that decoded string `<repeat_count>` times.
   - Example: `2:QUJDfDEyMw==` decodes to `ABC|123` and should be emitted twice.
3. **Format Conversion & Filtering**: 
   - The decoded strings are pipe-separated (`|`) records with the fields: `timestamp|sensor_id|value|status`.
   - Filter the records so you *only* keep rows where the `status` column is exactly `CRITICAL`.
   - Convert the pipe-separated `|` delimiters to comma-separated `,` delimiters for these filtered records.
4. **Consolidation**:
   - Collect all the filtered, comma-separated records from all `.cst` files.
   - Create a final consolidated file at `/home/user/summary/critical_sensors.csv`.
   - The final CSV file **must** have a header row: `timestamp,sensor_id,value,status`
   - The data rows must be sorted chronologically by the `timestamp` column (oldest to newest).

Ensure you use proper streaming/piping to handle the data, as the real dataset could be large (even though this sample might be small). You are free to use a combination of Python, bash, `awk`, `sed`, or `sort` to accomplish this.