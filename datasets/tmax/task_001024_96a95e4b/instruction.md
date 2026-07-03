You are a data scientist working with raw IoT sensor datasets. You need to build a C++ data processing pipeline to clean, resample, normalize, and extract features from a noisy temperature and humidity dataset.

The raw data is located at `/home/user/raw_sensor_data.csv`. It has the following columns: `time_min` (integer, minutes from start), `temperature` (float), and `humidity` (float). The data has irregular sampling intervals (missing minutes).

Your objective is to write, compile, and execute a C++ program (`/home/user/sensor_pipeline.cpp`) that performs the following steps:

1. **Resampling & Gap-filling**: 
   - Read the input CSV.
   - Resample the data to 1-minute intervals from the minimum `time_min` to the maximum `time_min`.
   - For missing minutes, linearly interpolate both `temperature` and `humidity` based on the nearest surrounding valid data points.

2. **Normalization**:
   - Calculate the mean and *population* standard deviation (divide by N, not N-1) for both gap-filled `temperature` and `humidity`.
   - Create normalized versions of these columns using Z-score standardization: `z = (x - mean) / std_dev`.

3. **Feature Extraction**:
   - Calculate a 5-minute rolling mean for the *normalized* temperature and humidity.
   - The 5-minute rolling mean at time `t` should be the average of the normalized values from `t-4` to `t` inclusive. If fewer than 5 data points are available (e.g., at the start of the series), calculate the average over all available points up to `t`.

4. **Output Generation**:
   - Write the processed dataset to `/home/user/processed_features.csv` with the following exact columns: `time_min,norm_temp,norm_hum,roll_mean_temp,roll_mean_hum`.
   - Format all float outputs to exactly 4 decimal places.

5. **Pipeline Logging**:
   - Generate a JSON log file at `/home/user/pipeline_log.json` tracking the pipeline statistics. It must have the following exact structure:
     ```json
     {
       "total_rows_input": <int>,
       "total_rows_output": <int>,
       "temperature_mean": <float, 4 decimal places>,
       "temperature_stddev": <float, 4 decimal places>,
       "humidity_mean": <float, 4 decimal places>,
       "humidity_stddev": <float, 4 decimal places>
     }
     ```

Ensure you install any necessary C++ build tools (e.g., `g++`) to compile your program. The final state of the system must contain the executable, the output CSV, and the log JSON file in `/home/user`.