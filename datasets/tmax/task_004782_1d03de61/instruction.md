You are an AI assistant acting as a data scientist. You have been given a messy CSV file containing sensor logs, but the standard tools are failing because some text fields contain embedded newlines, causing the parser to silently drop or corrupt rows.

Your task is to write a Go program (`/home/user/process_sensors.go`) that correctly parses, cleans, normalizes, deduplicates, and imputes missing values in this dataset.

**Input File:**
`/home/user/raw_sensor_data.csv`
It contains four columns: `timestamp`, `sensor_id`, `reading`, and `notes`.
The `notes` column is enclosed in quotes but frequently contains embedded newlines and erratic whitespace. The `reading` column contains floating-point numbers, but some values are missing (empty strings).

**Requirements for your Go program:**
1. **Parsing:** Safely parse the CSV, properly handling embedded newlines in the `notes` column.
2. **Deduplication:** If multiple rows have the exact same `timestamp` and `sensor_id` (case-insensitive during comparison), keep only the **first** one that appears in the file. Drop the subsequent duplicates.
3. **Normalization:**
   - Convert `sensor_id` to uppercase.
   - Tokenize and normalize the `notes` field by replacing any sequence of whitespace characters (spaces, tabs, newlines) with a single space character, and trim any leading/trailing whitespace.
4. **Imputation:** For any missing `reading` values (empty string), impute the missing value using the **mean** of all valid `reading` values for that specific `sensor_id` (calculated *after* deduplication). If a sensor has no valid readings at all, impute `0.00`.
5. **Sorting:** Sort the final cleaned data chronologically by `timestamp`. If timestamps are identical, sort alphabetically by the normalized `sensor_id`.
6. **Output:** Write the results to `/home/user/cleaned_sensor_data.csv`. 
   - Ensure the output includes the header row: `timestamp,sensor_id,reading,notes`.
   - Format the `reading` column to exactly two decimal places (e.g., `10.50`).

Write and execute the Go code to produce the cleaned dataset. Ensure the output strictly follows standard CSV quoting rules only when necessary.