You are a data engineer responsible for cleaning and transforming raw sensor logs into a reliable dataset for downstream modeling. 

You have a raw dataset located at `/home/user/raw_sensor_data.csv` containing IoT sensor readings with columns: `timestamp`, `sensor_id`, `temperature_c`, and `humidity`. The data is messy, containing missing values and extreme outliers due to sensor glitches.

Write and execute a reproducible Python ETL script at `/home/user/etl_pipeline.py` that processes the raw data according to the following strict rules:

1. **Filtering**: Drop any row where the `timestamp` is missing (empty or NaN).
2. **Outlier Handling**: For `temperature_c`, any value strictly greater than `80.0` or strictly less than `-30.0` is considered an anomaly. Treat these anomalies as missing values.
3. **Imputation**:
   - Impute missing values in `temperature_c` (including the anomalies you just neutralized) with the mean of the **valid** `temperature_c` readings for that specific `sensor_id`. Round the imputed values to 2 decimal places.
   - Impute missing values in `humidity` with the median of the **valid** `humidity` readings for that specific `sensor_id`. Round the imputed values to 1 decimal place.
4. **Feature Engineering**:
   - Create a new column `temp_f` which is the Fahrenheit conversion of the cleaned `temperature_c` (`C * 9/5 + 32`). Round this column to 2 decimal places.
   - Create a new column `hour_of_day` containing the integer hour extracted from the `timestamp` (0-23).
5. **Output**:
   - Sort the final dataset primarily by `timestamp` (ascending) and secondarily by `sensor_id` (ascending).
   - Save the cleaned dataset to `/home/user/clean_data.csv` with exactly the following columns in order: `timestamp,sensor_id,temperature_c,humidity,temp_f,hour_of_day`. Ensure `timestamp` is formatted as a standard ISO string (e.g., `YYYY-MM-DD HH:MM:SS` or similar standard pandas output). Do not include the dataframe index in the CSV.

Run your script to produce `/home/user/clean_data.csv`.