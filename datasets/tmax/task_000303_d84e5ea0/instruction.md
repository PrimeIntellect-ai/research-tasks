You are an AI assistant helping a data analyst fix a broken ETL pipeline and analysis script on a headless Linux server.

The previous analyst left a partially complete Python script (`/home/user/analyze.py`) that processes sensor data, but it is currently failing. The script is supposed to read data from `/home/user/raw_data.csv`, clean it, calculate an anomaly score using a specific formula, save a plot of the scores, and output the top anomalous events. 

However, the script has several issues:
1. It crashes because it tries to render a plot to a display (`plt.show()`), but this is a headless server.
2. The data cleaning (ETL schema enforcement) step is missing. The raw data contains some rows where the sensor values are the string `"ERR"` instead of floats.
3. The model inference step is missing. The formula for the anomaly score is documented in `/home/user/model_spec.txt`.

Your task is to fix and complete the pipeline. Specifically:
1. Install any necessary Python packages (e.g., `pandas`, `numpy`, `matplotlib`).
2. Update `/home/user/analyze.py` to enforce the data schema: drop any rows in the CSV where `sensor_a`, `sensor_b`, or `sensor_c` cannot be parsed as a float.
3. Compute a rolling covariance between `sensor_a` and `sensor_b` using a rolling window of size 3 (the current row and the 2 previous rows). For the first two valid rows where a window of 3 is not possible, the rolling covariance should be `0.0`.
4. Reconstruct the model architecture to compute the `anomaly_score` for each row based on the formula in `/home/user/model_spec.txt`.
5. Fix the plotting issue: configure `matplotlib` to use a headless backend (e.g., `Agg`) and save the plot to `/home/user/anomaly_plot.png` instead of trying to display it.
6. Create a JSON file at `/home/user/top_anomalies.json` containing a list of the 3 `timestamp` strings with the highest `anomaly_score`, ordered from highest to lowest.

Format of `top_anomalies.json` should be exactly:
```json
[
  "2023-01-01T05:00",
  "2023-01-01T02:00",
  "2023-01-01T10:00"
]
```

You can execute commands, modify the script, and run it to produce the expected output files.