You are a data scientist tasked with cleaning and reshaping a batch of time-series sensor data. 

We have a compressed dataset located in a simulated remote directory at `/home/user/remote_data/sensor_dump.tar.gz`. The archive contains a single CSV file named `raw_sensors.csv`. 

Previous attempts to process this data using basic command-line tools failed because the dataset contains a `remarks` column with embedded newlines inside quoted strings. Naive line-by-line processing silently drops or corrupts these rows.

Your task is to build a robust Python pipeline to process this data. Perform the following steps:

1. **Transfer and Extract**: Copy `sensor_dump.tar.gz` to your working directory at `/home/user/workspace/` (create this directory) and extract it.
2. **Clean & Normalize**:
   - Parse the CSV correctly, preserving data in rows with embedded newlines.
   - Remove any exact duplicate rows.
   - Normalize the `timestamp` column. The raw data contains mixed formats (e.g., `MM/DD/YYYY HH:MM`, `YYYY-MM-DD HH:MM:SS`). Convert all timestamps to standard ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`.
   - In the `remarks` column, replace any embedded newlines (`\n` or `\r\n`) with a single space.
3. **Reshape (Wide to Long)**:
   - The original CSV is in wide format with columns: `timestamp, sensor_alpha, sensor_beta, sensor_gamma, remarks`.
   - Melt/reshape the dataset into a long format. The new columns must be exactly: `timestamp`, `sensor_name`, `value`, `remarks`.
   - The `sensor_name` column should contain the strings `"sensor_alpha"`, `"sensor_beta"`, or `"sensor_gamma"`.
4. **Filter & Output**:
   - Drop any rows in the long-format dataset where `value` is missing (empty or NaN).
   - Sort the final dataset first by `timestamp` (ascending), then by `sensor_name` (ascending).
   - Save the fully processed dataset as a standard CSV at `/home/user/workspace/processed_sensors.csv` (include headers, comma-separated, without an index column).

Ensure your script handles the operations efficiently and correctly outputs the finalized CSV to the exact path specified.