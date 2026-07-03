You are a data analyst tasked with processing a set of environmental sensor readings from an experimental greenhouse. The data is provided in a CSV file at `/home/user/sensor_data.csv` and contains three columns: `timestamp` (in ISO 8601 format, e.g., `2023-10-01T14:32:15`), `temperature` (in Celsius), and `humidity` (in percentage).

Due to network issues, the sensor readings were logged at irregular intervals, and some hours have no data at all. You need to write a script in the language of your choice (Python, Perl, Ruby, etc.) to process this data and generate a daily summary report.

Please perform the following steps:

1. **Time-based Bucketing & Aggregation:** 
   Group the data into strict hourly buckets based on the timestamp (e.g., any time from `2023-10-01T08:00:00` to `2023-10-01T08:59:59` falls into the `2023-10-01T08` bucket). For each hourly bucket, calculate the arithmetic mean of the `temperature` and `humidity` values.

2. **Interpolation and Imputation:**
   Determine the full continuous range of hours from the earliest hour bucket present in the dataset to the latest hour bucket present. Some hours in this range will have no data. Fill in the missing hourly values for both `temperature` and `humidity` using linear interpolation between the nearest non-empty adjacent hourly buckets.

3. **Feature Extraction:**
   For every hour in the continuous range (both original and interpolated), calculate a new feature called the `stress_index` using the following formula:
   `stress_index = (temperature * 1.5) + (humidity * 0.5)`

4. **Daily Aggregation and Text Generation:**
   Group the hourly data (including the interpolated hours) by calendar day (e.g., `2023-10-01`). For each day, find the maximum `stress_index`.
   Finally, generate a report file at `/home/user/daily_report.txt`. For each day in chronological order, write exactly one line using the following template:
   `Date: YYYY-MM-DD - Max Stress Index: {value}`
   
   Replace `{value}` with the maximum stress index for that day, rounded to exactly two decimal places (e.g., `Date: 2023-10-01 - Max Stress Index: 84.25`).

Ensure your final report is saved to `/home/user/daily_report.txt`.