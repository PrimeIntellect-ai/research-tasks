You are a data analyst tasked with processing messy, wide-format IoT sensor time-series data using C++. 

You have been provided with an input file at `/home/user/input_data.csv`. This file contains timestamped temperature (T) and humidity (H) readings from multiple sensors. The format is wide and contains missing values (represented by empty fields between commas).

Example of input format:
```csv
timestamp,S1_T,S1_H,S2_T,S2_H
1000,20.5,50.0,22.1,55.0
1010,,51.0,22.5,
```

Your objective is to write a C++ program (`/home/user/process_sensors.cpp`), compile it to `/home/user/process`, and execute it to transform the data into a clean, long-format CSV file saved at `/home/user/output_data.csv`.

Your C++ program must perform the following pipeline:
1. **Wide-to-Long Reshaping:** Convert the row-based wide format into a long format where each row represents a single sensor's readings at a specific timestamp.
2. **Sorting:** Sort the flattened data first by `sensor_id` (alphabetically ascending, e.g., S1, S2), and then by `timestamp` (numerically ascending).
3. **Imputation (Forward Fill):** Many temperature and humidity values are missing (empty strings). Impute missing values using forward filling (carry over the last known valid value for that specific sensor). If the very first reading for a sensor is missing, default it to `0.00`.
4. **Feature Extraction:** Create a new column `temp_roll_avg_3`. This should be the rolling average of the current and up to two previous *imputed* temperature readings for that specific sensor. If fewer than 3 readings exist so far for a sensor, average the available ones.
5. **Validation & Output:** Write the final dataset to `/home/user/output_data.csv` with the exact header: `timestamp,sensor_id,temperature,humidity,temp_roll_avg_3`. 
   - All floating-point numbers must be formatted to exactly 2 decimal places.

To complete the task, your compiled executable `/home/user/process` must read `/home/user/input_data.csv` and successfully generate `/home/user/output_data.csv` matching all the rules above.