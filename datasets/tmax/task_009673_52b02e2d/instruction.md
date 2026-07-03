You are a data engineer building an ETL pipeline to process IoT telemetry data. You have been provided a SQLite database at `/home/user/data/telemetry.db` containing raw device logs.

The database has two tables:
1. `devices`: 
   - `id` (TEXT, Primary Key)
   - `firmware_version` (TEXT)
   - `region` (TEXT)
2. `logs`:
   - `id` (INTEGER, Primary Key)
   - `device_id` (TEXT)
   - `payload` (TEXT)

The `payload` column stores JSON strings representing document-based NoSQL logs. An example payload looks like this:
`{"timestamp": 1690000000, "sensor_readings": [{"type": "temperature", "value": 22.5}, {"type": "humidity", "value": 55.0}]}`

Your task is to complete the following:

1. **Index Strategy Design:** The `logs` table is currently unindexed and large. Create a SQL script at `/home/user/optimize.sql` that adds the necessary index(es) to optimize joining the `logs` table with the `devices` table on `device_id`. Execute this script against the database.

2. **Cross-Query Aggregation via Rust:** 
   Initialize a new Rust project at `/home/user/etl_processor` (using Cargo). 
   Write a Rust program in this project that connects to the SQLite database (e.g., using the `rusqlite` crate) and performs a complex query/aggregation.
   
   The program must:
   - Use SQLite's JSON1 extension functions (`json_each`, `json_extract`, etc.) directly in the SQL query to parse the `sensor_readings` array from the NoSQL `payload`.
   - Filter only for sensor readings where the `type` is exactly `"temperature"`.
   - Join this extracted data with the `devices` table.
   - Group the results by `region`.
   - Calculate the **maximum** temperature reading for each region.
   
3. **Output Generation:**
   The Rust program must output the final summarized results to a JSON file located at `/home/user/region_summary.json`. 
   The format must be a single JSON object where the keys are the region names and the values are the maximum temperatures (as floats). 
   Example format:
   `{"North": 45.2, "South": 48.1, "East": 42.0, "West": 41.5}`

Execute your Rust program to generate the `/home/user/region_summary.json` file. Ensure your code handles database connections safely and outputs valid JSON.