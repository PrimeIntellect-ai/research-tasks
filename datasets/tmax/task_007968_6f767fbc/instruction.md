You are a data analyst troubleshooting a fleet of industrial sensors. You have a large log file located at `/home/user/sensor_data.csv`. 

The file has no header and uses the format: `timestamp,sensor_id,status_msg,reading`
Where:
- `timestamp` is an integer UNIX epoch.
- `sensor_id` is an alphanumeric string (e.g., S1, S2).
- `status_msg` is a string message.
- `reading` is a floating-point number.

Your objective is to build a data processing pipeline that filters, sorts, and calculates rolling statistics on this data. You must use standard shell commands alongside a custom **C program** that you write to achieve this.

Here are the requirements:
1. **Filter (Regex Pattern Construction):** Use shell tools to extract only the rows where the `status_msg` strictly matches the format `ERROR-` followed exactly by a 3-digit uppercase hexadecimal code (e.g., `ERROR-1A4`, `ERROR-B22`, `ERROR-000`).
2. **Sort and Group (Large-scale sorting):** Sort the filtered data first by `sensor_id` alphabetically, and then by `timestamp` in ascending numerical order.
3. **Calculate Rolling Statistics:** Write a C program at `/home/user/rolling_stat.c` and compile it to `/home/user/rolling_stat`. This program should read the filtered and sorted CSV data from standard input (stdin). For each `sensor_id` group, calculate a rolling average of the `reading` column using a window size of exactly 3. 
   - If a sensor has 1 reading so far, the average is just that reading.
   - If it has 2 readings, the average is the mean of those two.
   - If it has 3 or more, the average is the mean of the latest 3 readings.
   - The rolling window must reset completely when encountering a new `sensor_id`.
4. **Output format:** Your C program should print the results to standard output, formatted as: `sensor_id,timestamp,rolling_avg`. The `rolling_avg` must be printed to exactly two decimal places (e.g., `15.00`).

Run your pipeline and save the final output to `/home/user/processed_data.csv`. 

Ensure your C program handles standard CSV lines gracefully and does not hardcode data limits if possible.