You are a data engineer tasked with building an ETL pipeline to process raw sensor data. 

The raw data is located at `/home/user/data/raw_sensor.csv`. However, this data has several issues:
1. It is encoded in `ISO-8859-1` and contains special characters that must be converted to `UTF-8`.
2. It has missing readings. The sensor should record data every 1 minute, but there are gaps in the timestamps.
3. Some rows are completely empty.

We have a proprietary time-series gap-filling tool, `ts_filler`, whose source code is vendored at `/app/ts_filler-1.2`. 
You need to compile this tool and use it in your pipeline. `ts_filler` reads a UTF-8 CSV from standard input and writes the gap-filled CSV to standard output. 
However, it seems the tool is currently producing sub-optimal results (it fills missing values with zeros instead of performing linear interpolation, which is required for our downstream models). You will need to inspect the vendored package, find the misconfiguration causing this behavior, fix it, and recompile the tool.

Your final objective is to create a bash script at `/home/user/etl.sh` that does the following:
1. Cleans the raw data (handles the character encoding conversion to UTF-8 and removes completely empty rows).
2. Processes the cleaned data through the fixed and compiled `ts_filler` tool to resample and fill gaps via linear interpolation.
3. Includes a validation checkpoint before outputting: if any resulting `value` is negative, the script should fail (exit code 1).
4. Saves the final processed data to `/home/user/final.csv`.

Requirements:
- Your script `/home/user/etl.sh` must be executable.
- The output `/home/user/final.csv` must be a valid UTF-8 CSV with the filled time-series data.
- You must achieve a high accuracy on the filled values (Mean Squared Error vs. the true sensor readings must be less than 0.1).

Do not rely on external downloads for the gap-filling tool; you must use and fix the vendored `ts_filler` package in `/app/ts_filler-1.2`.