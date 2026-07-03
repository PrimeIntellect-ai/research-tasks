You are an automation specialist building a data processing pipeline using only Bash and standard Linux utilities (like `awk`, `sed`, `grep`, `sort`, etc.). 

You are provided with a raw sensor dataset at `/home/user/raw_sensors.csv`. The file has the following header:
`timestamp,sensor_id,temperature,comments`
The timestamps are in the format `YYYY-MM-DDTHH:MM:SS`.

This dataset has several data quality issues:
1. Some "comments" fields contain embedded newlines, which split single records across multiple lines. 
2. There are missing values in the `temperature` column.

Write a Bash script at `/home/user/process.sh` that performs the following pipeline exactly in this order:

1. **Filtering**: Read `/home/user/raw_sensors.csv`. Silently drop any physical line that does not contain exactly 3 commas. This effectively removes header, malformed lines, and fragments of rows containing embedded newlines.
2. **Gap-Filling (Resampling)**: For the remaining valid lines, if the `temperature` field (the 3rd column) is empty, replace it with the most recently observed valid `temperature` in the file. You can assume the very first valid row always has a temperature value.
3. **Aggregation**: Group the data by the hour (extract `YYYY-MM-DDTHH` from the timestamp). Calculate the mean (average) temperature for each hour using the gap-filled values.
4. **Standardization (Min-Max Scaling)**: Find the minimum and maximum hourly mean temperatures across the entire aggregated dataset. Create a new column that normalizes these hourly means to a 0.0 to 1.0 scale using the formula `(mean - min) / (max - min)`. If max equals min, the normalized value should be 0.0000.
5. **Formatting**: Output the final results to `/home/user/processed_hourly.csv`. The output must be sorted chronologically by the hour. The file must not have a header. Each line should be formatted exactly as:
`YYYY-MM-DDTHH,mean_temperature,normalized_temperature`
Format both numeric values to exactly 4 decimal places.

**Constraints:**
- You must write the solution entirely in `/home/user/process.sh` and it must be executable.
- Do not use Python, Perl, or other higher-level scripting languages. Rely on shell built-ins, `awk`, `sed`, etc.
- Make sure to execute your script so the final output file `/home/user/processed_hourly.csv` is generated.