You are a data engineer building an ETL pipeline to process text data from an older sensor network.

The raw data is located at `/home/user/input/sensor_log.csv`. 
This file has several quirks you must handle:
1. It is encoded in UTF-16LE.
2. It is a comma-separated file, but the `raw_log` column contains multi-line strings with embedded newlines.
3. The columns are: `id`, `category`, `temp_c`, `pressure_psi`, `raw_log`.

Write a Python script that performs the following ETL steps and saves the final result to `/home/user/processed_data.json`:

1. **Extraction & Encoding:** Read the CSV correctly, preserving the embedded newlines in the `raw_log` column without dropping rows or misaligning columns.
2. **Information Extraction:** Extract the 8-character status code from the `raw_log` column using a regular expression. The code always follows the pattern "CODE: " followed by 3 uppercase letters, a hyphen, and 4 digits (e.g., "CODE: SYS-0001"). Create a new column called `status_code` containing just this 8-character identifier (e.g., "SYS-0001").
3. **Reshaping:** Convert the data from wide to long format. Melt the `temp_c` and `pressure_psi` columns into two new columns: `metric_name` (which will contain the strings "temp_c" or "pressure_psi") and `metric_value` (containing the corresponding numerical values).
4. **Stratified Sampling (Deterministic):** To downsample the data for downstream testing, group the reshaped data by `category`. For each category, keep exactly the first 4 rows when sorted by `id` (ascending) and then by `metric_name` (ascending). 
5. **Output:** Save the resulting dataset as a JSON array of objects to `/home/user/processed_data.json`. The output must be valid UTF-8. The keys in each JSON object must be exactly: `id`, `category`, `status_code`, `metric_name`, `metric_value`. All values should be strings, except `id` which should be an integer, and `metric_value` which should be a float.

Do not use any external orchestration tools; a single Python script executed in the terminal is sufficient.