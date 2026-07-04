You are a data engineer building an ETL pipeline to ingest IoT sensor data. 

You have received a raw data file located at `/home/user/raw_sensors.csv`. This file is encoded in ISO-8859-1 (Latin-1), not UTF-8. It contains historical sensor readings with four columns: `seq_id` (integer), `timestamp` (string), `location_name` (string), and `reading` (float). 

Unfortunately, the data has two major issues:
1. **Encoding:** The `location_name` field contains special characters (like accents) that are encoded in ISO-8859-1.
2. **Missing Data:** Some of the `reading` values are missing (represented by empty fields in the CSV, e.g., `...,Location,,`). 

Your task is to write a C++ program and execute shell commands to complete the following ETL pipeline:

**Step 1: Data Transformation (C++)**
Write a C++ program `/home/user/etl_processor.cpp` that:
* Reads `/home/user/raw_sensors.csv`.
* Converts all text from ISO-8859-1 to standard UTF-8.
* Imputes missing `reading` values using **linear interpolation**. The file is guaranteed to be ordered by `seq_id`. If a reading is missing, compute its value based on the nearest preceding and succeeding valid readings in the file (regardless of location). For example, if `seq_id` 1 has reading 10.0, `seq_id` 2 is missing, and `seq_id` 3 has reading 20.0, the imputed value for `seq_id` 2 should be 15.0. (Assume the first and last rows will always have valid readings).
* Writes the cleaned, UTF-8 encoded, fully imputed data to `/home/user/clean_sensors.csv`.

Compile your code using `g++ -std=c++17 /home/user/etl_processor.cpp -o /home/user/etl_processor` and run it.

**Step 2: Database Bulk Import**
Using the `sqlite3` command-line tool, create an SQLite database at `/home/user/sensor_data.db`.
* Create a table named `readings` with the schema: `seq_id INTEGER, timestamp TEXT, location_name TEXT, reading REAL`.
* Bulk import the contents of `/home/user/clean_sensors.csv` into this table. 

**Step 3: Verification**
To verify your pipeline, run an SQLite query to calculate the average `reading` (rounded to 2 decimal places) for the location named `Café_Étoile` (ensure the UTF-8 matches exactly). Output only this numeric value to `/home/user/verification.log`.