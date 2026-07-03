You are a data engineer tasked with building an ETL pipeline to process messy IoT sensor data. 

We have received batch data from three different legacy sensors, stored in `/home/user/sensor_data/`. The data is messy, uses different character encodings, and has irregular sampling intervals.

Your objective is to write a Python script (e.g., `process_etl.py`) that reads, cleans, resamples, and summarizes this data. You must implement this using parallel processing (e.g., `concurrent.futures` or `multiprocessing`) to process the files concurrently.

**Input Data Specifications:**
The directory `/home/user/sensor_data/` contains three CSV files:
1. `sensor_A.csv` (UTF-8 encoding)
2. `sensor_B.csv` (UTF-16 encoding)
3. `sensor_C.csv` (ISO-8859-1 encoding)

Each CSV has the following columns: `timestamp` (YYYY-MM-DD HH:MM:SS format), `sensor_id`, `temperature`, `humidity`.

**Processing Requirements:**
1. **Parallel Execution:** You must process the three files in parallel.
2. **Encoding Handling:** Your script must correctly read each file using its respective encoding.
3. **Data Validation:** Before resampling, filter out invalid sensor readings:
   - `temperature` must be between -50.0 and 150.0 (inclusive).
   - `humidity` must be between 0.0 and 100.0 (inclusive).
   - Drop any rows violating these constraints or containing null/NaN values.
4. **Resampling & Gap-Filling:** For each sensor:
   - Set the `timestamp` column as a DatetimeIndex.
   - Resample the time series into strictly 5-minute intervals (e.g., 00:00, 00:05, 00:10).
   - Aggregate the data within each 5-minute bin by taking the **mean** of the values.
   - If a 5-minute bin is completely empty, gap-fill it using **forward fill** (`ffill()`) from the previous valid 5-minute bin. Do not backfill. If the very first bin is empty, leave it as NaN, but ensure subsequent empty bins are forward-filled.
5. **Combine:** Concatenate the cleaned, resampled dataframes from all sensors into a single DataFrame. Reset the index so `timestamp` becomes a regular column again.

**Output Requirements:**
1. Save the final combined DataFrame as a Parquet file at `/home/user/output/clean_data.parquet`.
2. Generate a Markdown report at `/home/user/output/report.md` using the following exact template (replace the bracketed placeholders with the calculated values from your final combined DataFrame):

```markdown
# ETL Processing Report
Total sensors processed: {total_sensors}
Total valid records after resampling: {total_records}
Sensor with highest average temp: {hottest_sensor_id}
Average temp of hottest sensor: {hottest_sensor_avg_temp}
```
*Note: Format the `{hottest_sensor_avg_temp}` to exactly 2 decimal places.*

Create the `/home/user/output/` directory if it does not exist. Your solution should be robust and self-contained. Run your script to generate the final outputs.