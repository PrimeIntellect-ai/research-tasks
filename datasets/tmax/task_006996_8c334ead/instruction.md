You are tasked with building a local ETL pipeline and performing a rigorous statistical analysis on a batch of simulated IoT sensor data. 

You have been provided with a directory containing several raw CSV files at `/home/user/raw_data/`. Each CSV contains raw sensor readings with the following columns: `timestamp` (string/datetime), `sensor_id` (string), and `value` (float).

Your objectives are:

1. **ETL Pipeline**:
   - Write a Python script that reads all CSV files in `/home/user/raw_data/`.
   - Clean the data by dropping any rows where `value` is missing (NaN) or `sensor_id` is empty.
   - Load this cleaned data into a SQLite database located at `/home/user/sensor_data.db`.
   - The database must have a table named `readings` with columns: `timestamp` (TEXT), `sensor_id` (TEXT), and `value` (REAL).

2. **Bootstrap Correlation Analysis**:
   - Write a separate Python script that queries the SQLite database to pivot the data so that rows are unique `timestamp`s, and columns are the `value`s for each `sensor_id`. (Assume timestamps align perfectly across sensors for the sake of this analysis).
   - Use a **bootstrap resampling method** to calculate the Pearson correlation coefficient between all pairs of sensors.
   - Bootstrap parameters: 
     - Iterations: 500
     - Sample size: Same as the number of rows in the pivoted dataset (sample with replacement).
     - Random seed: Use `np.random.seed(42)` immediately before the bootstrapping loop so the results are reproducible.
   - For each pair of sensors (e.g., `S_2` and `S_7`), calculate the mean correlation coefficient across all 500 bootstrap iterations, as well as the 95% confidence interval (the 2.5th and 97.5th percentiles of the bootstrap distribution).

3. **Reporting**:
   - Filter the results to only include sensor pairs where the **absolute value** of the mean correlation is greater than `0.75`.
   - Save these highly correlated pairs to a JSON file at `/home/user/correlated_sensors.json`.
   - The JSON must be a list of objects with exactly these keys: `sensor_a`, `sensor_b`, `mean_corr`, `ci_lower`, `ci_upper`.
   - To ensure a unique representation, ensure `sensor_a` is lexicographically smaller than `sensor_b` (e.g., "S_2" comes before "S_7"). Sort the final list by `sensor_a`, then `sensor_b`.
   - Round the `mean_corr`, `ci_lower`, and `ci_upper` values to exactly 3 decimal places.

Example output format for `/home/user/correlated_sensors.json`:
```json
[
  {
    "sensor_a": "S_2",
    "sensor_b": "S_7",
    "mean_corr": 0.852,
    "ci_lower": 0.812,
    "ci_upper": 0.884
  }
]
```

Please complete the pipeline and ensure the SQLite database and JSON report are correctly generated.