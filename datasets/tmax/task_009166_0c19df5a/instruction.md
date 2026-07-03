You are an automation specialist tasked with building a robust data processing pipeline for our new smart building IoT system. The sensors frequently drop packets, resulting in missing data and irregular timestamps, but our HVAC control systems require regular, clean data to operate efficiently.

A raw dataset has been dumped to `/home/user/raw_sensor_data.csv`. It contains four columns: `timestamp` (ISO8601), `sensor_id`, `temperature`, and `humidity`. 

Please write and execute a Python script to process this data. You will likely need to install required libraries like `pandas`.

Your pipeline must perform the following steps:

1. **Interpolation and Imputation**: Group the data by `sensor_id`. The dataset contains missing values (`NaN` or empty strings) for temperature and humidity. Interpolate these missing values using time-based linear interpolation. If there are leading/trailing missing values that cannot be interpolated, use forward-fill, then backward-fill.
2. **Time-based Bucketing**: Resample the cleaned data into regular 15-minute intervals (e.g., `00:00:00`, `00:15:00`) for each `sensor_id`. Use the mean of the data points within each 15-minute bucket. If a 15-minute bucket contains no data points, forward-fill the values from the previous bucket.
3. **Windowed Aggregation**: Calculate a 1-hour rolling average (which equals exactly 4 periods of 15-minute buckets) for both temperature and humidity, for each sensor. The window should require a minimum of 1 period to calculate a value (i.e., `min_periods=1`).
4. **Summary Statistics**: Calculate the daily minimum, maximum, and mean of the *1-hour rolling average* temperature and humidity for each sensor.

**Outputs required:**

1. **`/home/user/processed_rolling.csv`**: A CSV file containing the bucketed and rolling data. 
   - Columns must be exactly: `timestamp` (in ISO8601 format, e.g., `2023-10-01T00:00:00`), `sensor_id`, `temperature_bucketed`, `humidity_bucketed`, `temp_rolling_1h`, `hum_rolling_1h`.
   - Sort the output by `sensor_id` ascending, then `timestamp` ascending.

2. **`/home/user/daily_summary.json`**: A JSON file containing the daily summary statistics. The structure must be nested as follows:
   ```json
   {
     "YYYY-MM-DD": {
       "SENSOR_ID": {
         "temp_rolling_min": float,
         "temp_rolling_max": float,
         "temp_rolling_mean": float,
         "hum_rolling_min": float,
         "hum_rolling_max": float,
         "hum_rolling_mean": float
       }
     }
   }
   ```
   *Note: Extract the date string (YYYY-MM-DD) from the 15-minute interval timestamps.*
   Round all float values in the JSON to 2 decimal places.

Ensure your environment is set up properly and execute the script to generate these output files.