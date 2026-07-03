You are a data analyst tasked with processing a messy CSV file containing sensor readings and text comments. The data pipeline needs to clean the text, validate the numerical constraints, calculate a rolling statistic, and ensure proper character encoding.

The raw data file is located at `/home/user/raw_data.csv`.

Here are your requirements:
1. **Character Encoding:** The `raw_data.csv` file was exported from a legacy Windows system and is encoded in `cp1252`. You must read it using this encoding. 
2. **Constraint-based Validation:** The column `sensor_value` contains numeric readings. Valid readings must be strictly between `0.0` and `100.0` (inclusive). Drop any rows that contain invalid or missing `sensor_value`s.
3. **Text Normalization:** The `comment` column contains messy text. Normalize it by:
   - Converting all text to lowercase.
   - Replacing any sequence of multiple whitespace characters (spaces, tabs, etc.) with a single space.
   - Stripping leading and trailing whitespace.
4. **Rolling Statistics:** Add a new column named `rolling_avg` that calculates the rolling average of the `sensor_value` over a window of 3 rows (the current valid row and the up to 2 preceding valid rows). For the first two valid rows, use the available valid rows (i.e., `min_periods=1`). Round the `rolling_avg` to exactly 2 decimal places.
5. **Output:** Save the processed dataset to `/home/user/processed_data.csv`. The output file must be a CSV file encoded in `utf-8`. Include the header. It should contain exactly the columns: `timestamp`, `comment`, `sensor_value`, and `rolling_avg` in that order.

Please write and execute a Python script to perform this data processing task.