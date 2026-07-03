I am working on a data pipeline to track sensor experiments, but my analysis script is completely broken. I have three datasets from different sensor modules:
- `/home/user/sensor_A.csv`
- `/home/user/sensor_B.csv`
- `/home/user/sensor_C.csv`

I wrote a script at `/home/user/run_analysis.py` that is supposed to:
1. Load all three datasets.
2. Join them using an inner join on the time series index. 
3. Enforce a strict numeric schema by converting all sensor readings to floats, dropping any rows with missing or invalid values (like the string `'N/A'`).
4. Calculate the Pearson correlation matrix between the 5 sensor variables: `temp`, `pressure`, `humidity`, `vibration`, `light`.
5. Save the correlation matrix to `/home/user/correlation_matrix.csv`.
6. Save a visual heatmap of the matrix to `/home/user/heatmap.png`.

However, the script has several issues:
- It crashes when trying to join the data because of schema mismatches (e.g., column names).
- It doesn't properly handle the invalid strings in the data, causing the correlation math to fail or produce garbage.
- Due to a misconfiguration with matplotlib in my headless environment, it either crashes or produces a completely blank `heatmap.png`.

Please fix `/home/user/run_analysis.py` and run it so that it successfully outputs both the correct `/home/user/correlation_matrix.csv` and a valid, non-blank `/home/user/heatmap.png`. Do not hardcode the expected outputs; your script must compute them from the CSV files. 

The output `correlation_matrix.csv` must include the row index (sensor names) and the columns must be ordered exactly as: `temp`, `pressure`, `humidity`, `vibration`, `light`.