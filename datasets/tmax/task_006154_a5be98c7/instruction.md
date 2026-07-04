You are a data engineer responsible for building an ETL pipeline to process time-series data from an industrial machine. The raw data consists of irregularly sampled sensor readings and state change logs. 

You need to write a Python script (or use bash CLI tools, though Python is highly recommended for pandas capabilities) to process this data, align the time series, compute summary statistics, and output a structured JSON report.

**Input Data:**
The raw data is located in `/home/user/raw_data/`:
1. `/home/user/raw_data/sensor.csv` - Contains columns: `timestamp`, `temperature_celsius`. The readings are irregularly spaced.
2. `/home/user/raw_data/state.csv` - Contains columns: `timestamp`, `machine_state`. Records are only generated when the machine changes state (e.g., ON, OFF, ERROR).

**Processing Requirements:**
1. **Resampling & Gap-Filling (Sensor Data):** 
   - Resample the sensor data into exactly 1-minute intervals (using the start of the minute, e.g., `2023-10-01 10:00:00`).
   - The value for a 1-minute bin should be the **mean** of all readings that occurred during that minute.
   - If a minute bin has no readings, forward-fill (ffill) the temperature from the previous minute, but **limit the forward fill to a maximum of 2 consecutive minutes**. If a gap is larger than 2 minutes, the remaining bins should be `null` (NaN).

2. **Resampling & Gap-Filling (State Data):**
   - Align the state data to the same 1-minute interval bins.
   - The state for a given minute bin is the most recently recorded state exactly at or before that minute mark. 
   - Forward-fill the state indefinitely to cover the bins. 
   - Any minute bins before the very first state log should be treated as having an `"UNKNOWN"` state.

3. **Joins/Merges:**
   - Merge the resampled sensor data and the resampled state data on the 1-minute timestamps. Perform an inner join on the time index bounds (i.e., from the first minute bin of the sensor data to the last minute bin of the sensor data).

4. **Summary Statistics:**
   - Group the merged dataset by `machine_state`.
   - For each state, calculate the **mean** temperature across all 1-minute bins assigned to that state (ignoring `null`/NaN values). Round the result to 2 decimal places.
   - Count the total number of 1-minute bins assigned to each state (including bins where temperature is `null`).

**Output Specification:**
Create an ETL pipeline that produces a JSON file at `/home/user/pipeline/stats.json`. The JSON file must match this exact schema:

```json
{
  "summary_by_state": {
    "ON": {
      "mean_temperature": 45.67,
      "total_minutes": 15
    },
    "OFF": {
      "mean_temperature": 22.10,
      "total_minutes": 5
    },
    ...
  }
}
```
*(Note: Replace the values above with the actual calculated results. Exclude any states that have 0 total minutes in the merged time window).*

Create the directory `/home/user/pipeline/` if it does not exist, and write the final output there. You may create and run intermediate Python scripts to achieve this.