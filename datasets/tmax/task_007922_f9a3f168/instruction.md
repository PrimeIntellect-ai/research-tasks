You are a data engineer building the testing phase of an ETL pipeline. You have been provided with two datasets in your home directory: `/home/user/raw_sensor.csv` and `/home/user/target.csv`.

Your task is to write and execute a script (using Python, bash, or any available tool) that performs the following steps:
1. Read the raw sensor data from `/home/user/raw_sensor.csv`.
2. Group the data by `sensor_id` and aggregate the `reading_1` and `reading_2` columns by calculating their mean for each sensor.
3. Engineer a new feature for each sensor named `reading_diff`, which is the absolute difference between the mean of `reading_1` and the mean of `reading_2`.
4. Join this aggregated data with the target values found in `/home/user/target.csv` using `sensor_id`.
5. Calculate the Pearson correlation coefficient between your engineered feature `reading_diff` and `target_value`.
6. Save the final Pearson correlation coefficient (rounded to 3 decimal places) to a file named `/home/user/correlation_result.txt`. The file should contain only the numerical value.

File formats:
- `/home/user/raw_sensor.csv` columns: `timestamp`, `sensor_id`, `reading_1`, `reading_2`
- `/home/user/target.csv` columns: `sensor_id`, `target_value`