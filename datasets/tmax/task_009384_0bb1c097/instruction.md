You are a data analyst troubleshooting a performance issue with a local data pipeline. We have two large CSV datasets that contain IoT sensor metadata and temporal readings. Currently, querying the latest readings per sensor type and location is extremely slow and occasionally times out due to locked transactions.

Your task is to build an optimized Python script to load, index, and query this data using SQLite, utilizing its JSON capabilities to mimic a NoSQL document aggregation format for the final output.

Here are the requirements:
1. You will find two CSV files in `/home/user/`: `sensors.csv` and `readings.csv`.
2. Write a Python script named `/home/user/process_data.py` that:
   - Connects to an SQLite database at `/home/user/sensor_data.db`.
   - Creates two tables: `sensors` and `readings`.
   - Loads the data from the CSV files into these tables.
   - Creates appropriate **indexes** to optimize the following query requirement (preventing full table scans).
   - Constructs a **complex query (using joins and subqueries/window functions)** to find the single *most recent* reading (based on `timestamp`) for each `location_id` and `sensor_type` combination.
   - Formats the output conceptually like a NoSQL document aggregation: each row should be aggregated into a JSON array of objects representing the final results.
   - Saves the final aggregated JSON array to `/home/user/aggregated_output.json`.
3. To prove your index strategy works, your script must also execute an `EXPLAIN QUERY PLAN` for your complex query and save the raw string output to `/home/user/query_plan.txt`.

Constraints:
- You must use standard Python 3.x libraries (e.g., `sqlite3`, `csv`, `json`).
- Do not use ORMs like SQLAlchemy; write raw SQL.
- The output JSON in `/home/user/aggregated_output.json` must be a list of dictionaries with exactly these keys: `location_id`, `sensor_type`, `latest_timestamp`, `reading_value`.
- The query plan in `/home/user/query_plan.txt` must demonstrate the use of your indexes (it should not exclusively rely on `SCAN TABLE`).

Execute your script to produce the database, the query plan, and the final JSON output.