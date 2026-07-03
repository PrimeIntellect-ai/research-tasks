You are acting as an AI assistant for a climate researcher who needs to organize a messy, denormalized dataset into a properly structured relational database for efficient querying.

The researcher has collected climate sensor data into a raw SQLite database located at `/home/user/raw_data.db`. 
Currently, it contains a single denormalized table named `raw_readings` with the following schema:
`sensor_id` (TEXT), `sensor_model` (TEXT), `location_name` (TEXT), `latitude` (REAL), `longitude` (REAL), `timestamp` (INTEGER), `temperature` (REAL), `humidity` (REAL).

Your task is to write a Rust program that normalizes this data, applies an optimized index strategy, and outputs a schema validation report.

Perform the following steps:
1. Initialize a new Rust binary project at `/home/user/climate_processor`. You may use the `rusqlite` crate (version "0.31.0" or similar) and `serde_json` for JSON output.
2. The program must read from `/home/user/raw_data.db` and create a new, normalized database at `/home/user/normalized_data.db`.
3. Analyze the schema and map relationships to create the following normalized tables in the new database (enforce foreign keys):
   - `locations`: `id` (INTEGER PRIMARY KEY), `name` (TEXT UNIQUE), `latitude` (REAL), `longitude` (REAL)
   - `sensors`: `id` (TEXT PRIMARY KEY), `model` (TEXT)
   - `readings`: `id` (INTEGER PRIMARY KEY), `sensor_id` (TEXT) referencing `sensors(id)`, `location_id` (INTEGER) referencing `locations(id)`, `timestamp` (INTEGER), `temperature` (REAL), `humidity` (REAL).
4. Migrate all data from `raw_data.db` into `normalized_data.db`. Make sure `locations` and `sensors` only contain unique entries.
5. Design and apply an index strategy. Create indexes on the `readings` table to optimize the following two specific access patterns:
   - Pattern A: Quickly retrieving all readings for a given `location_id`, sorted by `timestamp` in descending order. Name this index `idx_readings_loc_time`.
   - Pattern B: Quickly filtering readings by `sensor_id`. Name this index `idx_readings_sensor`.
6. Output Schema Validation: Have your Rust program query the `sqlite_master` table of `normalized_data.db` to extract the `sql` definitions of all tables and indexes. Write these SQL strings into a JSON array and save it to `/home/user/schema_validation.json`.

Ensure your project compiles and runs successfully. The final state should have the populated `normalized_data.db` and the `schema_validation.json` file present in `/home/user/`.