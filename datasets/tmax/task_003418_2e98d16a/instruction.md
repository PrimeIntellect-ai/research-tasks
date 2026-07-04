You are a data scientist cleaning a raw environmental dataset using bash utilities. 

You have a dataset located at `/home/user/raw_sensors.csv` in a "wide" format.
The file contains a header and the following comma-separated columns:
`sensor_id,date,metric,v0,v1,v2,v3,v4,v5`

The columns `v0` through `v5` represent readings taken in 4-hour time buckets throughout the day:
- `v0` = `00-04`
- `v1` = `04-08`
- `v2` = `08-12`
- `v3` = `12-16`
- `v4` = `16-20`
- `v5` = `20-24`

Your task is to write a bash pipeline (using tools like `awk`, `grep`, `sort`, etc.) that does the following:
1. **Wide-to-Long Reshaping:** Conceptually unpivot the data so that each time bucket and its value is a separate record.
2. **Constraint-based Validation:** Discard any individual reading that is negative (e.g., `-999`, which indicates a sensor error).
3. **Time-based Aggregation:** Calculate the average valid reading for each `metric` and `time_bucket` combination across all sensors and dates.
4. **Sorting:** Sort the final output first by `metric` (alphabetically, ascending), and then by the calculated average value (numerically, descending).
5. **Formatting:** Round the average values to exactly 2 decimal places.

Write the final output to `/home/user/clean_aggregated.csv`.
The output file should NOT contain a header.
The format of the output file must be exactly:
`metric,time_bucket,avg_value`

Example of expected output format:
```
humidity,04-08,86.50
humidity,00-04,81.00
temp,12-16,18.53
temp,16-20,16.50
```