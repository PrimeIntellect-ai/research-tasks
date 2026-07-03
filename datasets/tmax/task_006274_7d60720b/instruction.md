You are a data analyst tasked with processing IoT sensor readings. You have a raw CSV file located at `/home/user/raw_sensors.csv` that contains timestamped temperature readings from three sensors in a "wide" format. Some data points were dropped during transmission and appear as empty strings.

Write a Go program (save it as `/home/user/process.go` and run it) to perform the following data pipeline operations:

1. **Wide-Long Format Reshaping:** Convert the data from its wide format (`timestamp`, `temp_A`, `temp_B`, `temp_C`) into a long format. The long format should logically have the columns: `timestamp`, `sensor_id`, `raw_value`.

2. **Interpolation and Imputation:** There are missing values in the data. For each sensor independently, sort the data chronologically and use "forward-fill" imputation (replace a missing value with the most recent previous valid value for that specific sensor). If the very first value for a sensor is missing, impute it with `0.0`.

3. **Normalization:** After imputation, perform Min-Max normalization for each sensor independently. Scale each sensor's values to a `[0.0, 1.0]` range using the formula `(value - min) / (max - min)`. If `max == min`, the normalized value should be `0.0`.

4. **Output CSV:** Write the reshaped, imputed, and normalized data to `/home/user/processed_sensors.csv`. 
   - Headers must be exactly: `timestamp,sensor_id,normalized_value`
   - Order the rows first by `timestamp` (ascending), then by `sensor_id` (alphabetical).
   - Format `normalized_value` to exactly 4 decimal places.

5. **Template-Based Text Generation:** Using Go's `text/template` package, generate a markdown summary report at `/home/user/sensor_report.md` based on the imputed (pre-normalized) values. The markdown file must exactly match this structure:

```markdown
# Sensor Report

## Sensor temp_A
- Min: [min_value formatted to 1 decimal place]
- Max: [max_value formatted to 1 decimal place]
- Data Points: [total number of points including imputed]
- Latest Normalized: [latest chronologically normalized value formatted to 4 decimal places]

## Sensor temp_B
...
(Repeat for all sensors in alphabetical order)
```

Ensure your Go program completes all these steps and creates both `/home/user/processed_sensors.csv` and `/home/user/sensor_report.md`.