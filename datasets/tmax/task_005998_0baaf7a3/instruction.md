You are acting as a data science assistant for a researcher organizing and benchmarking dataset inference speeds. 

The researcher has two CSV files containing performance logs from a recent experiment:
1. `/home/user/sensors.csv`: Contains metadata about the sensors (`sensor_id`, `model_type`). The `model_type` is either `Alpha` or `Beta`.
2. `/home/user/readings.csv`: Contains the actual reading logs (`sensor_id`, `reading_time_ms`, `value`). `reading_time_ms` simulates the inference performance speed of the sensor's internal model.

Your task:
1. Ensure required Python packages for data manipulation and statistical analysis (e.g., `pandas`, `scipy`) are installed. 
2. Write and execute a Python script that joins these two datasets on `sensor_id`.
3. Calculate the mean `reading_time_ms` for both `Alpha` and `Beta` model types.
4. Perform an independent two-sample t-test (assuming unequal variances / Welch's t-test) comparing the `reading_time_ms` of the `Alpha` models against the `Beta` models to test the hypothesis that their inference speeds differ.
5. Save the results to `/home/user/report.txt` in the exact format shown below, with all floating-point numbers rounded to exactly 4 decimal places.

Required format for `/home/user/report.txt`:
```
Mean Alpha: <value>
Mean Beta: <value>
T-statistic: <value>
P-value: <value>
```

Note: If you run into environment issues with `pip`, you may use `--break-system-packages` or a virtual environment, but ensure the final script executes successfully and produces the report file.