You are managing a system's configuration tracking pipeline. System parameters are logged sporadically into a text file whenever a configuration change occurs. You need to analyze the `MAX_MEM` parameter to detect anomalous jumps by comparing the daily values against a rolling average.

The log file is located at `/home/user/sys_config.log`. Each line contains three space-separated fields: `Day_Index` (integer), `Parameter_Name` (string), and `Value` (integer). 
Note that days without a configuration change are omitted from the log.

Your task is to write a Bash script (using standard CLI tools like `awk`, `sed`, `bash`) to perform the following operations:

1. **Extract and Gap-Fill (Resampling)**: Filter the records for the `MAX_MEM` parameter. Find the minimum and maximum `Day_Index` for `MAX_MEM`. For every day between the minimum and maximum (inclusive), determine the active `MAX_MEM` value. If a day is missing from the log, use the value from the most recent preceding day that has a logged value (forward-filling).
2. **Rolling Statistics**: For each day starting from the 3rd day of your continuous sequence (i.e., Day `min + 2` up to Day `max`), compute a 3-day rolling average. The 3-day rolling average for Day `N` is the arithmetic mean of the filled `MAX_MEM` values on Day `N-2`, Day `N-1`, and Day `N`.
3. **Distance Calculation**: Calculate the absolute distance (difference) between the actual filled `MAX_MEM` value on Day `N` and its 3-day rolling average.
4. **Output Generation**: Write the results to `/home/user/anomalies.txt`. Output one line per day (starting from Day `min + 2`), formatted as `Day_Index Distance`. Format the `Distance` as a floating-point number rounded to exactly 2 decimal places (e.g., `0.00`, `3.33`).

Example output format for `/home/user/anomalies.txt`:
```
3 3.33
4 0.00
5 60.00
```

Ensure your operations are primarily implemented via Bash and standard Linux text processing utilities. Create and execute the script to generate the final output file.