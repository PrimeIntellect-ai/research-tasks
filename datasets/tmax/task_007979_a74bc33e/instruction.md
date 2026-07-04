You are a compliance officer investigating a potential insider threat. You have been provided with two data extracts from your organization's systems: an organizational hierarchy dump in JSON format (`/home/user/org_chart.json`) and a NoSQL-style document dump of system access logs (`/home/user/access_logs.json`).

Your objective is to write a multi-purpose Bash script, `/home/user/audit.sh`, that accepts a single employee ID as a parameter and generates an anomaly report for that employee and all of their direct and indirect subordinates.

Here are the requirements for your script:

1. **NoSQL-style Aggregation with jq**:
   The `access_logs.json` contains a flat array of JSON objects. Each object has `user_id`, `timestamp` (ISO 8601), `action`, and `bytes`. 
   Use `jq` to filter out any records where the `action` is "blocked", and then transform the remaining data into a CSV format (`user_id,timestamp,bytes`) saved temporarily.

2. **Hierarchical Parsing**:
   The `org_chart.json` is a nested JSON object representing the company structure. Every node has an `id` and a `subordinates` array.
   You must extract a flattened list of all employee-to-manager relationships into a CSV format (`employee_id,manager_id`). Note that the top-level employee has no manager (represented as an empty string or NULL).

3. **Relational Database Setup**:
   Create a local SQLite database at `/home/user/audit.db`. Import the flattened organization relationships and the filtered access logs into two tables: `org` and `logs`.

4. **Recursive and Analytical Queries**:
   Your script must execute a parameterized SQL query against `/home/user/audit.db` using the employee ID provided as the first argument to the script (e.g., `./audit.sh E01`).
   The query must:
   - Use a **Recursive CTE** to find the provided employee and ALL of their direct and indirect subordinates.
   - For this subset of employees, use a **Window Function** to calculate a rolling sum of `bytes` transferred by each user within a 15-minute sliding window (based on the `timestamp`). You will likely need to cast the timestamps to unix epochs for the window frame.
   - Flag any log entry where the rolling 15-minute sum of bytes strictly exceeds 5000.

5. **Output**:
   The script must output the flagged anomalies to `/home/user/flagged_<employee_id>.csv` (e.g., if the parameter is `E01`, the file should be `/home/user/flagged_E01.csv`).
   The CSV must have the header: `user_id,timestamp,rolling_bytes` and be sorted by `timestamp` ascending, then `user_id` ascending.

The execution of your script should be self-contained and run completely without user interaction.