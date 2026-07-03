You are an AI assistant helping a researcher organize and process a faulty sensory dataset. 

The researcher has a script that produces blank plots because the backend misconfigures the data scaling when it encounters NaNs and extreme outliers. Instead of fixing the plotting script directly, you need to preprocess the data into a clean, large-scale storage format (Parquet) and compute specific metrics to verify numerical stability.

There is a raw dataset located at `/home/user/sensor_data.csv` with columns `timestamp`, `sensor_A`, and `sensor_B`.

Write a Python script (you can name it `/home/user/process_data.py`) to perform the following exact steps:

1. **Missing Value Handling**: Read the CSV. The `sensor_A` column contains missing values (`NaN`). Fill these missing values using linear interpolation (direction: forward, default pandas `interpolate(method='linear')`).
2. **Outlier Handling**: The `sensor_B` column contains extreme sensor glitches. Clip the values of `sensor_B` so that any value below the 1st percentile or above the 99th percentile of the *original* `sensor_B` column is replaced by the 1st and 99th percentiles, respectively. Use the `pandas` default percentile computation (linear interpolation).
3. **Feature Engineering & Numerical Accuracy**: Create a new column named `signal_ratio`. This should be calculated exactly as: `sensor_A / (sensor_B + 0.001)`. To ensure numerical accuracy and consistency across different architectures, round the `signal_ratio` column to exactly 4 decimal places.
4. **Data Storage**: Save the final cleaned dataframe (with all 4 columns: `timestamp`, `sensor_A`, `sensor_B`, `signal_ratio`) to a Parquet file at `/home/user/clean_sensors.parquet`.
5. **Verification Log**: Calculate the mean of the `signal_ratio` column. Write this single floating-point number (rounded to 4 decimal places) to a log file at `/home/user/metrics.log`.

Execute your script to produce the output files.