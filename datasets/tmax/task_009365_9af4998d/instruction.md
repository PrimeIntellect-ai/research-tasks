You are a data engineer tasked with building a lightweight ETL pipeline. 

You have a directory containing several large simulated sensor logs in CSV format located at `/home/user/sensor_data/`. Each file is named `sensor_<id>.csv` (e.g., `sensor_1.csv`) and contains two columns: `timestamp` (integer) and `temperature` (float). The data in each file is sorted by timestamp.

Your task is to write a Python script at `/home/user/process.py` that performs the following:
1. **Parallel Processing:** Uses Python's `multiprocessing` or `concurrent.futures` module to process all CSV files in the `/home/user/sensor_data/` directory concurrently.
2. **Windowed Aggregation:** For each sensor, calculates a rolling 3-reading simple moving average (SMA) of the `temperature`. The moving average should only be calculated when there are at least 3 readings available (i.e., the first output value will correspond to the 3rd timestamp).
3. **Multi-format Transformation:** Writes the final aggregated data out to a single JSON file at `/home/user/sensor_summary.json`. 

The output JSON must have the following structure:
```json
{
  "sensor_1": [
    {"timestamp": 3, "sma": 22.0},
    {"timestamp": 4, "sma": 24.5}
  ],
  "sensor_2": [
    ...
  ]
}
```
*Note: Round the `sma` values to 2 decimal places.*

Ensure your code is efficient, handles the data streamingly where possible (treating it as if the files were extremely large), and correctly combines the parallel results into the single target output file. Run your script to produce the output file.