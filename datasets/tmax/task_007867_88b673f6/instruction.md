You are a data scientist responsible for cleaning daily raw sensor data and moving it into a structured database for analysis, while quarantining bad data.

A daily dump of CSV files is located in `/home/user/raw_data/`. You need to build a Python script at `/home/user/process_data.py` to orchestrate a data pipeline that validates the data, bulk-imports valid records into an SQLite database, and exports invalid records to a quarantine file.

**Input Data Description:**
The CSV files in `/home/user/raw_data/` have the following header:
`sensor_id,timestamp,temperature,humidity,status`

**Validation Constraints:**
A row is considered **valid** only if ALL the following constraints are met:
1. `sensor_id`: Must exactly match the regex `^SN-\d{4}$` (e.g., SN-1024).
2. `timestamp`: Must be a valid ISO8601 string in the exact format `YYYY-MM-DDTHH:MM:SSZ`. (You only need to check the format structure, not calendar validity like leap years).
3. `temperature`: Must be a valid float between `-40.0` and `85.0` (inclusive).
4. `humidity`: Must be a valid float between `0.0` and `100.0` (inclusive).
5. `status`: Must be one of the exact strings: `ACTIVE`, `MAINTENANCE`, or `OFFLINE`.

**Pipeline Requirements:**
1. Your script `/home/user/process_data.py` must read all `.csv` files in `/home/user/raw_data/`.
2. Evaluate every row against the constraints above.
3. **For Valid Rows:** Bulk insert them into an SQLite database located at `/home/user/sensor_data.db`. 
   - Table name: `readings`
   - Schema: `sensor_id (TEXT), timestamp (TEXT), temperature (REAL), humidity (REAL), status (TEXT)`
   - Create the table if it does not exist. Do not wipe the table if it exists (append mode).
4. **For Invalid Rows:** Write them to a single JSON file located at `/home/user/quarantine.json`.
   - The JSON file must contain a single JSON array of objects.
   - Each object must contain the original key-value pairs from the CSV row.
   - Additionally, each object must contain a key `"invalid_columns"`. Its value must be a sorted (alphabetical) list of strings, representing the names of the columns that failed validation (e.g., `["humidity", "temperature"]`). If a value fails parsing (e.g., cannot be converted to float), it is considered a constraint failure for that column.

Run your script so that the database and JSON file are populated.