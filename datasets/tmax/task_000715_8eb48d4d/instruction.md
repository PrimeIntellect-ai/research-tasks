You are an engineer tasked with building a configuration tracker. System configurations over time have been dumped into various formats in the `/home/user/inputs/` directory. 

Your goal is to write a Python script that reads these files, filters out invalid configurations, deduplicates them, and loads the valid, unique records into a centralized SQLite database.

**Input Files:**
You have three files in `/home/user/inputs/`:
1. `snapA.json` (JSON format, array of objects)
2. `snapB.csv` (CSV format with headers)
3. `snapC.xml` (XML format, `<configs>` root containing `<config>` elements)

Every record across all formats represents a configuration snapshot and has the following fields: `server_id` (string), `service` (string), `port` (integer), `status` (string), and `config_string` (string).

**Processing Requirements:**
1. **Multi-Format Reading**: Parse all three files. Process them strictly in alphabetical order of their filenames (`snapA.json`, then `snapB.csv`, then `snapC.xml`). Within each file, process records in their top-to-bottom order.
2. **Constraint Validation**: Keep a record ONLY if it meets ALL of the following criteria:
   - `port` is an integer between `1024` and `65535` (inclusive).
   - `status` is exactly `"active"` or `"inactive"`.
3. **Hash-Based Deduplication**: For each valid record, compute an MD5 hash of the exact string formatted as `server_id|service|config_string` (e.g., `srv1|web|workers=4`). 
   - If multiple records produce the same MD5 hash, keep ONLY the first one encountered during your ordered processing. Discard subsequent duplicates.
4. **Database Bulk Export**: Create an SQLite database at `/home/user/master_config.db`.
   - Create a table named `valid_configs` with the exact schema: `(server_id TEXT, service TEXT, port INTEGER, status TEXT, config_string TEXT, config_hash TEXT)`.
   - Insert all valid, deduplicated records into this table, including their computed MD5 `config_hash`.

Complete this task by writing and executing a Python script that performs the above operations.