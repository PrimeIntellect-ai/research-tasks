You are acting as a Data Engineer and Analyst. We have a set of factory machines, and we need to build an end-to-end data processing, modeling, and benchmarking pipeline.

In `/home/user/data`, there are three CSV files:
1. `sensors.csv`: Contains `machine_id` (integer), `temp` (float), and `vibration` (float).
2. `maintenance.csv`: Contains `machine_id` (integer) and `days_since_last_service` (integer). Note: Not all machines have a maintenance record!
3. `labels.csv`: Contains `machine_id` (integer) and `failed` (integer, 0 or 1).

Your task is to write a Python script at `/home/user/pipeline.py` that does the following:

1. **Multi-source Data Joining**: 
   - Load the three CSV files.
   - Perform a left join starting from `sensors.csv`, bringing in `maintenance.csv` and then `labels.csv` using `machine_id` as the key.
   - *Crucial Data Type Handling*: Because not all machines have maintenance records, the join will introduce missing values (NaNs), which silently converts the `days_since_last_service` column to floats. You must fill these missing values with `-1` and explicitly convert the column back to a standard integer type (`int64`).
   - Save this cleaned and correctly typed dataframe to `/home/user/output/joined_data.csv` (do not include the pandas index in the output file).

2. **Classification**:
   - Split the joined data into features (`temp`, `vibration`, `days_since_last_service`) and the target (`failed`). Do not split into train/test (use the whole dataset for training for this exercise).
   - Train a standard `LogisticRegression` model from `scikit-learn` using default parameters.
   - Calculate the training accuracy.

3. **Inference Performance Benchmarking**:
   - We need to know how fast this model is for real-time scoring. 
   - Run inference (`model.predict()`) on the entire feature dataset 500 times in a loop.
   - Measure the total time taken for these 500 iterations, and calculate the average inference time **per single row** in microseconds (µs).

4. **Reporting**:
   - Create a JSON file at `/home/user/output/metrics.json` containing exactly two keys:
     - `"accuracy"`: The training accuracy as a float.
     - `"inference_micros_per_row"`: The average inference time per row in microseconds as a float.

Make sure to install any necessary packages (e.g., `pandas`, `scikit-learn`) before running your script. Create the `/home/user/output` directory if it does not exist.