You are a data engineer tasked with building an ETL pipeline to process environmental sensor telemetry. The raw data often contains missing values due to sensor dropout and lacks derived features required by the downstream machine learning models. 

You need to write a Python script at `/home/user/etl_pipeline.py` that processes the raw telemetry data.

**Input Data:**
A CSV file is located at `/home/user/raw_telemetry.csv` with the following columns: `timestamp,temperature,pressure`. The rows are uniformly spaced in time, but several `temperature` and `pressure` values are missing (empty strings/NaN).

**Processing Requirements:**
1. **Imputation:** Read the CSV. Impute missing `temperature` and `pressure` values using **Quadratic Polynomial Interpolation** (e.g., using pandas `interpolate(method='polynomial', order=2)`). 
2. **Feature Extraction:** Create a new column named `temp_roc` (Temperature Rate of Change). This should be the difference between the current row's interpolated `temperature` and the previous row's interpolated `temperature`. Fill the `temp_roc` for the first row with `0.0`.
3. **Data Formatting:** Round all float columns (`temperature`, `pressure`, `temp_roc`) to exactly 2 decimal places.
4. **Output:** Save the transformed dataset to `/home/user/clean_telemetry.csv` (keeping `timestamp,temperature,pressure,temp_roc`).

**Pipeline Logging Requirement:**
To ensure data quality is monitored, your script must output a structured JSON log file at `/home/user/pipeline_log.json` containing specific metrics about the run. The JSON must have the following exact keys and format:
```json
{
  "imputed_temperature_count": <integer, number of missing temperature values filled>,
  "imputed_pressure_count": <integer, number of missing pressure values filled>,
  "max_temp_roc": <float, the maximum rate of change in temperature across the dataset, rounded to 2 decimal places>
}
```

Run your script to produce the final `clean_telemetry.csv` and `pipeline_log.json` files.