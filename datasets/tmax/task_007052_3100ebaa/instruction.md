You are acting as a systems compliance officer. You have been tasked with auditing a massive, legacy SQLite database containing system access logs. 

The database is located at `/home/user/compliance.db`. It contains two tables:
1. `users` 
   - `uid` (INTEGER PRIMARY KEY)
   - `username` (TEXT)
   - `clearance_level` (INTEGER)
2. `logs`
   - `id` (INTEGER PRIMARY KEY)
   - `uid` (INTEGER)
   - `action` (TEXT)
   - `target_system` (TEXT)
   - `timestamp` (INTEGER)
   - `success` (INTEGER - 1 for success, 0 for failure)

Your task is to build a Rust reporting tool that identifies unauthorized access attempts and exports a structured summary. An unauthorized access attempt is defined as any log entry where `success = 0` AND the user's `clearance_level` is less than 3.

Please complete the following objectives:

1. **Create an Optimization Script**:
   Create a file at `/home/user/optimize.sql` containing a single SQL `CREATE INDEX` statement. This index should be specifically designed to optimize the querying of the `logs` table when filtering by `uid` and `success` status.

2. **Build the Rust Auditor Tool**:
   Initialize a Rust project at `/home/user/auditor`. 
   Write a CLI tool that takes a single user ID (`uid`) as a command-line argument.
   The tool must connect to `/home/user/compliance.db`, apply the index from `/home/user/optimize.sql` (execute the script), and then use a safely parameterized SQL query to join the `users` and `logs` tables.
   
   It must aggregate the total number of unauthorized access attempts per `target_system` for the specified `uid`. 
   
3. **Export the Results**:
   The Rust tool must export the results to `/home/user/report_<uid>.json` (e.g., if the CLI argument is `42`, the output should be `report_42.json`).
   The output must be a tightly formatted JSON array of objects, sorted alphabetically by `target_system`. 
   Format example:
   ```json
   [
     {"target_system": "Billing API", "unauthorized_attempts": 4},
     {"target_system": "Mainframe", "unauthorized_attempts": 1}
   ]
   ```

4. **Execute**:
   Once compiled, run your tool against `uid` 42. Verify that `/home/user/report_42.json` is generated successfully.