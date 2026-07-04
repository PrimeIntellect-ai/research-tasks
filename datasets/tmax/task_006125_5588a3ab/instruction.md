You are a data engineer building a robust ETL pipeline for a smart agriculture company. You have been tasked with processing raw time-series sensor data, performing quality checks, imputing missing values, and identifying redundant sensors based on their temperature profiles.

Your pipeline must perform the following tasks sequentially:

1. **Extract**: Raw sensor data is located in `/home/user/raw_data/`. Each file is a CSV named `sensor_<id>.csv` containing three columns: `timestamp`, `temperature`, and `moisture`. There are missing values in the `temperature` column (represented as empty strings).

2. **Validate (Quality Gate)**:
   - For each CSV file, check if the `temperature` column has strictly greater than `30%` missing values. 
   - If it does, the file fails the quality gate. Record the exact filename (e.g., `sensor_03.csv`) in a log file at `/home/user/output/rejected.log` (one filename per line) and do NOT process this sensor further.
   - If it passes, proceed to the next step.

3. **Transform (Imputation)**:
   - For sensors that pass the quality gate, sort the data chronologically by `timestamp`.
   - Impute missing values in the `temperature` column using linear interpolation.
   - If the very first or very last values are missing, use backward-fill (bfill) and forward-fill (ffill) respectively to ensure no NaN values remain.

4. **Transform (Distance Computation)**:
   - All sensors share the exact same set of timestamps. Extract the fully imputed `temperature` vectors for all valid sensors.
   - Compute the pairwise Euclidean distance between the `temperature` vectors of every possible pair of valid sensors.

5. **Load**:
   - Save the cleaned, imputed DataFrame for each valid sensor to `/home/user/output/cleaned/<sensor_id>.parquet` (e.g., `sensor_01.parquet`).
   - Identify all pairs of valid sensors where the Euclidean distance between their temperature vectors is strictly less than `15.0`.
   - Output these similar pairs to a JSON file at `/home/user/output/similar_sensors.json`. The JSON should be a list of lists. Each inner list must contain the two sensor IDs (without the `.csv` extension, e.g., `["sensor_01", "sensor_04"]`). 
   - Ensure each inner list is sorted alphabetically, and the outer list is sorted alphabetically by the first element of each inner list.

You will need to create the output directories if they do not exist. Write and execute a Python script to perform this entire ETL pipeline.