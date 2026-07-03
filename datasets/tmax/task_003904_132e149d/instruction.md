You are a data analyst tasked with processing messy IoT sensor data. 

We have a raw dataset located at `/home/user/raw_sensor_data.csv`. The data is currently in a wide format, where each column represents a different room's sensor, and the rows represent time intervals. The dataset contains several data quality issues:
- Temperature readings are stored as strings with units (e.g., "20.5 C").
- Some readings failed and are recorded as the string "ERR".

Your goal is to clean, impute, reshape, and calculate statistics on this data using Python. Write a script to perform the following operations:

1. **String Cleaning**: Strip the " C" from the temperature readings and convert the "ERR" values to actual null/NaN values. Convert the remaining string numbers to floats.
2. **Imputation**: Use linear interpolation to fill in the missing (NaN) temperature values for each sensor column.
3. **Reshaping**: Convert the dataset from wide format to long format. The resulting columns should be `timestamp`, `sensor`, and `temperature`. 
4. **Rolling Statistics**: For each individual sensor, calculate a rolling average of the `temperature` over a window of 3 periods (use `min_periods=1`). Name this new column `rolling_mean`.
5. **Output**: Save the final processed data to `/home/user/processed_sensor_data.csv`.

**Strict Requirements for the Output File:**
- The CSV must contain exactly these columns in order: `timestamp,sensor,temperature,rolling_mean`
- Sort the data first by `sensor` (alphabetical, ascending), then by `timestamp` (ascending).
- Format all floating-point numbers (`temperature` and `rolling_mean`) to exactly 2 decimal places (e.g., `20.50`, `22.33`).
- Do not include the DataFrame index in the CSV.

You may install any required Python packages (like pandas) using pip. Once you are done executing your script and generating the output file, you have completed the task.