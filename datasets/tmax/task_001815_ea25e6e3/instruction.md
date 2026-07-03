You are a data engineer responsible for building an ETL pipeline to process irregularly sampled, noisy data from environmental sensors in a server room. 

I have a raw CSV file at `/home/user/raw_sensors.csv` containing irregular timestamped data from two sensors: `temp_c` (temperature) and `humidity_pct`. The timestamps are in various formats and sometimes contain timezone offsets. There are gaps in the data.

Your task is to write a Python script at `/home/user/etl_pipeline.py` that performs the following steps:

1. **Extract and Align**: Load `/home/user/raw_sensors.csv`. Parse the `timestamp` column into UTC datetime objects.
2. **Resample and Aggregation**: Resample the data into exactly 5-minute intervals starting from `2023-10-01 10:00:00 UTC` to `2023-10-01 11:00:00 UTC` inclusive. Use the mean of the values if multiple readings fall into the same 5-minute bin. (Use left-labeling and left-closed bins).
3. **Interpolation**: There are gaps in the data where no readings occurred for a 5-minute bin. Fill these missing values (NaNs) using linear interpolation. 
4. **Database Bulk Import**: Save the cleaned, resampled, and interpolated dataframe to a local SQLite database at `/home/user/sensors.db`. Write the data to a table named `cleaned_data`. The table should have columns `timestamp` (as a string in 'YYYY-MM-DD HH:MM:SS' format), `temp_c` (float), and `humidity_pct` (float). 
5. **Template-Based Text Generation**: Use the `jinja2` library to generate a summary report. Create a file `/home/user/report.txt` containing exactly this structure, filled with the correct max and min values computed from your **cleaned** dataset (rounded to 1 decimal place):
```
Server Room Environmental Report
--------------------------------
Max Temperature: <MAX_TEMP> C
Min Temperature: <MIN_TEMP> C
Max Humidity: <MAX_HUMIDITY> %
Min Humidity: <MIN_HUMIDITY> %
```

You will need to install any necessary Python packages (like `pandas` and `jinja2`) yourself using pip.
Ensure your script executes successfully and creates both `/home/user/sensors.db` and `/home/user/report.txt` with the specified formats.