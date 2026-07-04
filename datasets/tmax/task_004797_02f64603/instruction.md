You are a data engineer building a mini ETL pipeline to process a batch of IoT sensor data. 

I have placed a dataset at `/home/user/sensor_data.csv`. The file has the following columns: `timestamp`, `sensor_id`, `temperature`, `humidity`.

Your task is to write a script in any language you prefer to process this data, validate it, compute some aggregations, and output the results to a specific JSON file.

Here are the processing rules:
1. **Data Validation**: Read the CSV. You must filter out (drop) any rows where the `temperature` is outside the range `[-20.0, 50.0]` (inclusive) OR the `humidity` is outside the range `[0.0, 100.0]` (inclusive). 
2. **Rolling Aggregation**: For each `sensor_id`, ordered chronologically by `timestamp` (the data is already sorted by time, but you should ensure chronological processing), compute a simple moving average (SMA) of the valid `temperature` readings using a rolling window of exactly 3 valid readings. Do not output values for windows smaller than 3. (e.g., the first output value for a sensor will be the average of its 1st, 2nd, and 3rd valid readings; the next is the 2nd, 3rd, and 4th, etc.). Round the averages to 1 decimal place.
3. **Summary Aggregation**: For each `sensor_id`, find the maximum `humidity` recorded across all of its *valid* readings. Round to 1 decimal place.

Write the final output to `/home/user/etl_output.json` with the exact following schema:

```json
{
  "rolling_temp_sma": {
    "S1": [22.0, 24.0, ...],
    "S2": [12.0, ...]
  },
  "max_humidity": {
    "S1": 80.0,
    "S2": 100.0
  }
}
```

Make sure the keys in the dictionaries are the actual `sensor_id`s present in the file. Ensure your script handles the entire file and produces `/home/user/etl_output.json`.