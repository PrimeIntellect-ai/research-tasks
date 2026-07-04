You are a Machine Learning Engineer tasked with preparing a training dataset for a legacy predictive model. The raw data comes from a high-frequency sensor array, but it is noisy, high-dimensional, and occasionally corrupted.

You need to build a C++ ETL pipeline that enforces the data schema, reduces the dimensionality of the features, and validates the final output before it is fed into the model.

**Input Data:**
There is a raw data file located at `/home/user/raw_sensors.csv`. It does not have a header.
The expected schema for each row is:
- Column 1: `sensor_id` (integer)
- Column 2: `timestamp` (string in the format YYYY-MM-DDTHH:MM:SS)
- Columns 3 through 32: 30 sensor readings (floating-point numbers)

**Requirements:**

1. **Schema Enforcement & Filtering (ETL Phase 1)**:
   Write a C++ program at `/home/user/etl_processor.cpp` that reads `/home/user/raw_sensors.csv`.
   If a row does not strictly adhere to the expected schema (e.g., it doesn't have exactly 32 columns, `sensor_id` is not a valid integer, or any sensor reading cannot be parsed as a float), the row must be skipped.
   Write the original text of all skipped rows into `/home/user/invalid_rows.log`, exactly as they appeared in the input, preserving the original order.

2. **Dimensionality Reduction (ETL Phase 2)**:
   For valid rows, reduce the 30 sensor readings into 3 aggregate dimensions using the following logic:
   - `dim1`: The **mean** of the first 10 sensor readings (Columns 3 to 12).
   - `dim2`: The **maximum** of the next 10 sensor readings (Columns 13 to 22).
   - `dim3`: The **minimum** of the final 10 sensor readings (Columns 23 to 32).

3. **Model Output Validation & Transformation**:
   The legacy model crashes if feature values exceed bounds or are undefined. Before outputting the reduced dimensions:
   - If any `dim` evaluates to NaN (Not-a-Number) or Infinity, drop the entire row (and append its original text to `/home/user/invalid_rows.log`).
   - Clamp all valid `dim1`, `dim2`, and `dim3` values to the range `[-100.0, 100.0]`. If a value is > 100.0, set it to 100.0. If it is < -100.0, set it to -100.0.

4. **Final Output**:
   Write the successfully processed rows to `/home/user/processed_features.csv`.
   The output must be a comma-separated file with no header.
   Format: `sensor_id,timestamp,dim1,dim2,dim3`.
   Format the floating-point dimensions to exactly 4 decimal places.

Compile your program using `g++ -O3 /home/user/etl_processor.cpp -o /home/user/etl_processor` and run it to produce the output files.