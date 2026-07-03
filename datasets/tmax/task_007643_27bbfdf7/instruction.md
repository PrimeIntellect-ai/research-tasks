You are a data engineer responsible for building a lightweight ETL pipeline to process time-series telemetry data from IoT sensors.

Your task is to write a Python script at `/home/user/run_pipeline.py` that processes a raw telemetry CSV file, normalizes the metrics, and generates a pipeline execution log. 

**Input Data:**
There is a file at `/home/user/raw_telemetry.csv` containing time-series data with the following columns: `timestamp`, `sensor_id`, `temperature`, `humidity`.

**Pipeline Requirements:**
1. **Data Normalization:**
   - Apply Z-score standardization to the `temperature` column. (Use `pandas` default `.mean()` and `.std()` methods, which use sample standard deviation `ddof=1`).
   - Apply Min-Max normalization to the `humidity` column. (Use `pandas` default `.min()` and `.max()` methods).
2. **Output Data:**
   - Save the fully processed dataset to `/home/user/normalized_telemetry.csv`. It should have the exact same columns and row order as the input, but with the `temperature` and `humidity` values replaced by their normalized/standardized counterparts. Keep float values exactly as computed by pandas.
3. **Pipeline Logging:**
   - The script must create a JSON log file at `/home/user/pipeline_metrics.json` to monitor the pipeline's execution.
   - The JSON file must have the following exact structure (populate the numeric values based on the *original* unnormalized data):
     ```json
     {
       "pipeline_status": "SUCCESS",
       "records_processed": <integer_number_of_rows>,
       "temperature_stats": {
         "mean": <float_mean_temp>,
         "std": <float_std_temp>
       },
       "humidity_stats": {
         "min": <float_min_humidity>,
         "max": <float_max_humidity>
       }
     }
     ```

**Execution:**
Once you have written the script, execute it so that the output files (`/home/user/normalized_telemetry.csv` and `/home/user/pipeline_metrics.json`) are generated successfully. Do not delete the original raw data file.