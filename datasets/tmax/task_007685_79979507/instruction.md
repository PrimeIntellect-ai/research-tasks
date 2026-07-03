You are a machine learning engineer tasked with preparing training data for a predictive model. You need to build a small ETL pipeline using Rust. 

We have a raw sensor dataset located at `/home/user/data/raw_sensors.csv` with the following columns: `timestamp`, `sensor_a`, `sensor_b`, and `sensor_c`. Some values are missing, and some values are outliers caused by sensor glitches.

Your task is to write a Rust program in `/home/user/etl_pipeline` that processes this CSV file and performs the following operations:

1. **Missing Value Handling**: Read the CSV. If `sensor_a` or `sensor_b` is missing (empty string), fill the missing value with `0.0`. Keep track of the total number of missing values filled across the dataset.
2. **Outlier Capping**: For `sensor_c`, any value strictly greater than `100.0` is an outlier. Cap these values at `100.0`. Keep track of how many outliers were capped.
3. **Linear Algebra Feature Extraction**: Use the Rust `ndarray` crate to compute a new feature called `sensor_proj`. For each row, treat `[sensor_a, sensor_b]` as a 1D array and compute its dot product with the weight vector `[0.5, 0.8]`.
4. **ETL Output**: Write the cleaned and transformed data to `/home/user/data/clean_sensors.jsonl` (JSON Lines format). Each line should be a JSON object with the exact keys: `"timestamp"` (integer), `"sensor_proj"` (float), and `"sensor_c"` (float).
5. **Experiment Tracking**: Write a summary JSON file to `/home/user/logs/experiment.json` containing the exact keys: `"total_rows"` (integer, total number of data rows processed), `"outliers_capped"` (integer), and `"missing_filled"` (integer).

You must:
- Initialize the Cargo project at `/home/user/etl_pipeline`.
- Use the `ndarray` crate for the dot product calculation.
- Compile and run your Rust program to generate the output files.

Make sure the output directories `/home/user/data` and `/home/user/logs` exist. Create them if they do not. The raw input data will be placed at `/home/user/data/raw_sensors.csv` before you begin.