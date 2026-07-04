You are an AI assistant helping a data researcher process and organize a set of sensor datasets. The researcher wants to build a data cleaning pipeline in Go that handles missing values, removes outliers, joins multiple sources, and tracks experiment metrics.

The researcher has placed two CSV files in the home directory:
1. `/home/user/sensor_data.csv`: Contains time-series sensor readings.
   Columns: `ID`, `Timestamp`, `Temperature`, `Humidity`
2. `/home/user/sensor_metadata.csv`: Contains metadata about the sensors.
   Columns: `ID`, `Location`, `Model`

Write a Go program located at `/home/user/cleaner.go` that performs the following steps:
1. Read and parse both CSV files.
2. Join the data on the `ID` column.
3. Handle missing values: Drop any row that has an empty value in any column (including missing temperature or humidity).
4. Handle outliers: Drop any row where the `Temperature` is strictly greater than 50.0 or strictly less than -10.0.
5. Write the cleaned and joined dataset to `/home/user/cleaned_data.csv`. The output CSV must include the header and columns in this exact order: `ID,Timestamp,Temperature,Humidity,Location,Model`.
6. Implement experiment tracking by writing a JSON file to `/home/user/experiment_metrics.json`. The JSON object must contain the following keys:
   - `"initial_rows"`: Integer. The total number of rows in the original `sensor_data.csv` (excluding the header).
   - `"rows_after_missing_drop"`: Integer. The number of rows remaining after dropping those with missing values.
   - `"rows_after_outlier_drop"`: Integer. The final number of rows remaining after outlier removal.
   - `"final_mean_temperature"`: Float. The arithmetic mean of the `Temperature` column for the final remaining rows.

You may use standard library packages. Compile and run your program to ensure the output files are correctly generated.