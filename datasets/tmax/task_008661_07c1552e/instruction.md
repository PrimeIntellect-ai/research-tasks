I am a researcher organizing a massive influx of environmental sensor data. Right now, I have a raw, messy dataset in `/home/user/raw_sensor_data.csv`. I need you to clean this dataset and organize it into a more efficient storage format.

Please do the following:
1. Setup a Python virtual environment in `/home/user/sensor_env` and install `pandas` and `pyarrow`.
2. Write and execute a Python script (using the environment you just created) to process `/home/user/raw_sensor_data.csv`. The CSV has the following columns: `timestamp`, `sensor_id`, `temperature`, `humidity`.
3. During processing, apply these cleaning rules:
   - Drop any rows that have missing (NaN or empty) values in ANY column.
   - Handle outliers for both `temperature` and `humidity` by clipping (capping/flooring) the values to their respective 1st and 99th percentiles. Compute these percentiles on the entire dataset *after* dropping the missing values.
4. Save the cleaned dataset as a partitioned Parquet dataset in the directory `/home/user/processed_sensors`. 
   - Partition the dataset by `sensor_id`. 
   - Ensure the output format is a directory of Parquet files organized as `/home/user/processed_sensors/sensor_id=.../`.

Your final output should be the successfully created Parquet dataset directory. No further reporting is needed, but the data must be strictly accurate based on the percentiles.