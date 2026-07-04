You are acting as a data analyst. We have a dataset of sensor readings in a CSV file, but our previous automated reporting script was silently ignoring data corruption and outputting completely wrong metrics (similar to a visualization script silently producing blank plots due to misconfigured backends).

I need you to write a robust Rust program that processes the data, strictly handles missing values and outliers, and computes the correct statistical summary.

The Rust project is located at `/home/user/sensor_analysis`. I have already created the `Cargo.toml` with the `csv` crate dependency.

The dataset is located at `/home/user/sensor_analysis/data.csv` with the following columns:
`id,sensor_a,sensor_b`

Your task:
1. Write the Rust code in `/home/user/sensor_analysis/src/main.rs`.
2. The code must parse `data.csv`.
3. Handle Missing Values: Completely drop any row where `sensor_a` or `sensor_b` is empty, `"NA"`, or cannot be parsed as a float.
4. Handle Outliers: Our sensors sometimes malfunction and record exactly `-9999.0`. Drop any row containing `-9999.0` in either sensor column.
5. Calculate the following statistics on the cleaned dataset:
   - Total number of valid rows
   - The sample mean of `sensor_a`
   - The sample mean of `sensor_b`
   - The Pearson correlation coefficient between `sensor_a` and `sensor_b`
6. The program must write these exact results to `/home/user/sensor_analysis/results.txt` in the following format (ensure float values are rounded to exactly 3 decimal places):
```
Valid rows: [COUNT]
Mean A: [MEAN_A]
Mean B: [MEAN_B]
Correlation: [CORRELATION]
```

Build and run your Rust program to ensure `results.txt` is generated correctly.