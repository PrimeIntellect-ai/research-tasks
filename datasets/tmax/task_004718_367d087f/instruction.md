You are a data scientist preparing a data-cleaning pipeline. Before building a heavy pipeline, you need to write a fast, Bash-native cleaning script to evaluate a basic anomaly detection algorithm on a raw sensor dataset. 

You have a dataset at `/home/user/sensor_data.csv` with the header `id,sensor_reading`.

Your task is to create a robust Bash script `/home/user/test_pipeline.sh` that performs the following steps:

1. **Numerical Configuration:** Ensure numerical operations use standard dot-decimal format by explicitly setting `LC_NUMERIC=C` in your script.
2. **Model "Training" (Parameter Calculation):** Read through the dataset and calculate the mean and population standard deviation of the `sensor_reading` column. 
   - **Ignore** the header.
   - **Ignore** any rows where `sensor_reading` is missing, NaN, or contains non-numeric characters (a valid reading matches the extended regular expression `^-?[0-9]+(\.[0-9]+)?$`).
3. **Inference / Filtering (Evaluation):** Make a second pass over the dataset. Filter out all invalid rows (as defined above) AND any rows where the absolute Z-score of the `sensor_reading` is strictly greater than `2.0`.
   - Z-score is calculated as: `(value - mean) / stddev`.
4. **Output Generation:** Save the cleaned dataset to `/home/user/clean_output.csv`, preserving the original header `id,sensor_reading` followed by the valid, non-anomalous rows in their original order.
5. **Inference Performance Benchmarking:** At the end of your script, benchmark the performance of this filtering logic. Run the filtering process (steps 2-4) 5 times in a loop. Measure the total real execution time of these 5 runs in seconds, and append a line to `/home/user/report.log` in this exact format:
   `Benchmark complete. 5 iterations took [X] seconds.` (where [X] is the total time to any precision).

Constraints:
- The script must be written in Bash and use standard POSIX utilities (like `awk`, `grep`, `sed`). You may not use Python, R, or Perl to solve this.
- Make sure `/home/user/test_pipeline.sh` is executable and run it to produce the outputs.