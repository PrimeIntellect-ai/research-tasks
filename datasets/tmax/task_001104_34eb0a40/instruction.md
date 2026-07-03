You are a data analyst working with a stream of sensor data. 

You have been provided with a CSV file at `/home/user/raw_sensors.csv`. This file contains data in a "wide" format, where each row represents a `timestamp` and subsequent columns (`S1`, `S2`, `S3`, `S4`, `S5`) represent readings from different sensors. 

Unfortunately, the data ingestion network occasionally drops packets, resulting in missing values (represented as empty strings in the CSV). You need to process this file to prepare it for a downstream database that requires "long" format data without missing values.

Write a Python script to process the data with the following requirements:
1. **Large-file streaming approach**: You must process the file iteratively or in chunks to minimize memory footprint, simulating how you would handle a file that is hundreds of gigabytes in size. Do not load the entire file into memory at once.
2. **Imputation**: For any missing value, impute it using linear interpolation based on the immediately preceding and succeeding timestamps for that specific sensor. You can safely assume that missing values never occur on the first or last row, and there are never two consecutive missing values for the same sensor.
3. **Reshaping**: Transform the data from its wide format into a long format with columns `timestamp`, `sensor`, and `value`.
4. **Aggregation**: After reshaping and imputing, calculate the total sum of all the `value`s across all sensors and timestamps.

Save the final total sum as an integer (or float rounded to 2 decimal places if there are fractions, though the data allows for exact integers) to `/home/user/result.txt`.