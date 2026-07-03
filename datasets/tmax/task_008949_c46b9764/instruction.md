You are a log analyst investigating patterns in a sporadically updated system log. The log file is located at `/home/user/system_metrics.log`. It contains unstructured text messages, but embedded within some lines are timestamps and specific numerical metric readings.

Your task is to write a Python script that processes this log file and generates a structured summary report.

Here are the requirements:
1. **Information Extraction:** Parse `/home/user/system_metrics.log`. Extract the timestamp (enclosed in brackets `[]` at the start of the line) and the floating-point value immediately following the exact string `METRIC_VAL: `. Ignore lines that do not contain `METRIC_VAL: `.
2. **Normalization:** Convert the extracted timestamps into standard datetime objects.
3. **Resampling and Gap-filling:** 
   - Aggregate the extracted metrics into strict 15-minute intervals. The bins should be labeled by their start time, closed on the left (e.g., a reading at `10:14:59` goes into the `10:00:00` bin). 
   - If multiple readings fall into the same 15-minute bin, take their arithmetic mean.
   - The time range for your bins must start exactly at `2023-10-01 10:00:00` and end at `2023-10-01 11:45:00` (inclusive of the 11:45:00 bin).
   - For any 15-minute interval that has no data, fill the gap by forward-filling (carrying over the value from the previous 15-minute interval). You may assume the first bin (`10:00:00`) will always have at least one reading.
4. **Template Generation:** Calculate the maximum metric value from your final resampled and gap-filled data. Generate a report exactly matching this template, and save it to `/home/user/report.txt`:

```
Log Analysis Report
===================
Start Time: 2023-10-01 10:00:00
End Time: 2023-10-01 11:45:00
Total Resampled Intervals: {interval_count}
Max Value (after gap-filling): {max_val}
```
Replace `{interval_count}` with the integer number of 15-minute intervals. Replace `{max_val}` with the maximum value rounded to 2 decimal places.

Do not use any external libraries other than `pandas` and built-in Python modules (like `re` or `datetime`).