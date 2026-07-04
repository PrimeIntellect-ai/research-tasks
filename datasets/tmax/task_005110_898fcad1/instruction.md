You are a data analyst for a meteorological research institute. We are receiving CSV telemetry data from a network of weather sensors, but we suspect that some malicious actors are injecting fabricated data into our data streams to skew our climate models.

Your task is to create a robust data processing pipeline in Python that cleans, filters, and standardizes the sensor data.

We have provided a proprietary, stripped legacy binary at `/app/telemetry_oracle` that our engineers previously used to validate the mathematical relationship between physical properties in the sensor readings. You must use this binary (or reverse-engineer its logic) to identify and drop fabricated records. 

Write a Python script at `/home/user/sanitize.py` that conforms to the following CLI signature:
`python3 /home/user/sanitize.py <input_csv_path> <output_csv_path>`

The script must perform the following operations in order:
1. **Read** the input CSV file. The CSV contains the following columns: `sensor_id`, `timestamp`, `temp_celsius`, `pressure_hpa`, `humidity_pct`.
2. **Deduplicate**: Remove duplicate rows, keeping only the first occurrence for any given combination of `sensor_id` and `timestamp`.
3. **Filter**: Evaluate each row's physical validity using the `/app/telemetry_oracle` binary. The binary takes three positional float arguments: `<temp_celsius> <pressure_hpa> <humidity_pct>`. It exits with code `0` if the reading is physically valid, and a non-zero exit code if it is physically impossible (fabricated). Drop all rows that are invalid.
4. **Summary Statistics & Normalization**: For the remaining valid rows, calculate the mean and sample standard deviation of the `pressure_hpa` column.
5. **Standardize**: Add a new column to the dataset named `pressure_zscore`. Calculate the Z-score for each valid row's pressure reading using the summary statistics computed in step 4. (If the standard deviation is 0, set the Z-score to 0).
6. **Output**: Save the cleaned, deduplicated, filtered, and standardized dataset to the specified `<output_csv_path>`. The output must include the CSV header. Round the `pressure_zscore` to 4 decimal places.

Ensure your script is robust, well-structured, and can process files efficiently. You may use standard Python libraries and `pandas` if desired.