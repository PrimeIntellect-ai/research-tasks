You are a data analyst tasked with processing a batch of noisy sensor data from an industrial IoT system. The data is located in `/home/user/sensor_data/` and consists of several CSV files, each corresponding to a unique machine sensor. 

The CSV files have the following columns: `timestamp`, `sensor_id`, `temperature`, `vibration`. 
Due to transmission errors, there are missing values (empty strings or 'NaN') in the `temperature` and `vibration` columns.

Your task is to write and execute a Python script at `/home/user/process.py` that reads these files, cleans the data, extracts specific features, and outputs a summary JSON file. Because the actual dataset can be large, **you must process the CSV files in parallel** using Python's `multiprocessing` or `concurrent.futures` modules (using multiple processes, not just threads).

Implement the following data processing pipeline for each file:
1. **Imputation & Interpolation**:
   - `temperature`: Fill missing values using linear interpolation based on the row order. If the first or last values are missing, fill them using a backward fill and forward fill, respectively, after the linear interpolation.
   - `vibration`: Fill missing values with the median value of the `vibration` column for that specific file.
2. **Feature Extraction**:
   After imputation, calculate the following features for the sensor:
   - `max_temperature`: The maximum temperature recorded (float).
   - `mean_vibration`: The average vibration recorded, rounded to 2 decimal places (float).
   - `temp_spikes`: The total count of rows where the `temperature` is strictly greater than `(mean_temperature_of_file + 2.0)` (integer).

Output the final aggregated results to `/home/user/summary.json`. The JSON file should be a dictionary where the keys are the `sensor_id`s, and the values are dictionaries of the extracted features.

Example output format for `/home/user/summary.json`:
```json
{
  "S01": {
    "max_temperature": 45.2,
    "mean_vibration": 12.33,
    "temp_spikes": 3
  },
  "S02": {
    ...
  }
}
```

Ensure your script is self-contained, installs any necessary dependencies (like `pandas`), runs the parallel processing, and successfully creates the output file.