You are a data analyst working with IoT sensor data. I have a raw CSV file containing temperature readings located at `/home/user/sensor_data.csv`. The file has three columns: `timestamp` (ISO 8601 format), `sensor_id`, and `temperature_c`. 

The data is messy: it contains duplicate records, readings from multiple sensors, and irregular recording intervals with some significant gaps.

Please write a Python script to process this data using the `pandas` library, and output the cleaned, aggregated results to `/home/user/hourly_summary.csv`.

Here are the exact requirements for your processing pipeline:
1. Filter the dataset to only include readings for `sensor_id` exactly equal to `A101`.
2. Remove any exact duplicate rows.
3. Resample the time series data into 1-hour buckets (e.g., `10:00:00`, `11:00:00`).
4. Calculate the mean `temperature_c` for each 1-hour bucket.
5. If there are any 1-hour buckets with no data (gaps in the time series between the minimum and maximum timestamps), impute the missing values using forward-fill (`ffill`).
6. Round the final mean temperatures to exactly 2 decimal places.

The output file `/home/user/hourly_summary.csv` must contain exactly two columns: `timestamp` and `avg_temp`. The `timestamp` should be formatted as `YYYY-MM-DD HH:MM:SS`. The header must be lowercase exactly as specified.