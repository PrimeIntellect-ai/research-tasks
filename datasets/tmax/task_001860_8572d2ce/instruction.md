You are a data scientist tasked with cleaning and processing a messy log file from an IoT sensor network. 

The raw data is located at `/home/user/raw_sensor_logs.txt`. It contains a mix of unstructured system messages and structured sensor readings.

Your objective is to build a Python pipeline that performs the following steps:
1. **Extraction**: Parse the log file and extract lines that contain sensor readings. Valid sensor reading lines look like this: `[YYYY-MM-DD HH:MM:SS] DEVICE_<ID> STATUS: <status> TEMP: <temp> HUM: <hum>`. Ignore any lines that do not match this format. Extract the Timestamp, Device ID, and Temperature.
2. **Grouping & Resampling**: Group the extracted data by Device ID. For each device, resample the temperature data to exactly 1-hour intervals (e.g., `2023-10-01 08:00:00`) by taking the **mean** of the temperatures within that hour. 
3. **Gap-Filling**: Use forward-filling (ffill) to fill any missing hourly intervals, but **limit the forward fill to a maximum of 2 consecutive hours**.
4. **Aggregation**: Calculate the daily maximum temperature for each device (resample to 1-day intervals).
5. **Quality Gate**: If any device has a daily maximum temperature strictly greater than `50.0` on *any* day, it is considered faulty. **Completely exclude** that device from the final output.
6. **Output**: Save the final cleaned data to `/home/user/daily_max_temp.json`. 

The JSON file should be structured as follows:
```json
{
  "DEVICE_01": {
    "2023-10-01": 26.0
  },
  "DEVICE_03": {
    "2023-10-01": 10.0,
    "2023-10-02": 12.0
  }
}
```
All temperatures must be rounded to 1 decimal place. Dates should be represented as strings in the `YYYY-MM-DD` format.

Ensure your code is reproducible and can be run via the terminal.