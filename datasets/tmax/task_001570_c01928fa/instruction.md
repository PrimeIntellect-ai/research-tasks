You are a data engineer tasked with building a multi-language ETL pipeline to process and validate sensor data.

We have a raw data file located at `/home/user/raw_sensor.csv` containing sensor readings. 

Your task is to:
1. Set up a Python virtual environment in `/home/user/venv` and install `pandas` and `scipy`.
2. Write a Python script `/home/user/process.py` that performs the following steps:
   a. Reads `/home/user/raw_sensor.csv`.
   b. Groups the data by `sensor_id`.
   c. Calculates the Z-score for the `reading` column within each group (using degrees of freedom = 0 for standard deviation).
   d. Filters out the outliers (keeps only rows where the absolute Z-score is <= 3.0).
   e. Saves the cleaned dataset to `/home/user/clean_data.csv` (keeping the original columns, without the z-score column).
3. Generate a validation report at `/home/user/report.txt` with exactly the following format:
```
Total original records: <original_count>
Total cleaned records: <cleaned_count>
Sensor 1 max clean reading: <sensor1_max_rounded_to_2_decimal_places>
Sensor 2 max clean reading: <sensor2_max_rounded_to_2_decimal_places>
```

Execute your script to produce `/home/user/clean_data.csv` and `/home/user/report.txt`. Ensure the report matches the required format precisely.