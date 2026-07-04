You are a data analyst tasked with processing a large CSV dataset of sensor logs, analyzing it via an optimized database schema, and writing a C application to export specific anomalous records.

You have been provided with a CSV file at `/home/user/sensors.csv`. The CSV has no header, but its columns are: `timestamp` (integer), `sensor_id` (text), `temperature` (real), `humidity` (real), and `status` (text).

Your objectives are:

1. **Database Setup & Import**:
   Create an SQLite database at `/home/user/sensor_data.db`. Create a table named `readings` with the appropriate schema for the columns described above, and import the CSV data into it.

2. **Index Strategy & Query Optimization**:
   We need to run the following query frequently:
   `SELECT sensor_id, temperature FROM readings WHERE status = 'ERROR' AND temperature > 80.0 ORDER BY timestamp DESC;`
   
   Create the most optimal index (or indices) for this specific query on the `readings` table. 
   Once created, use SQLite's `EXPLAIN QUERY PLAN` command for the above query and redirect the exact output to `/home/user/query_plan.txt`. The plan must show that your new index is being used to filter and order the results efficiently (without a separate sorting pass if possible).

3. **Query Result Export (C Program)**:
   Write a C program at `/home/user/exporter.c` that connects to `/home/user/sensor_data.db`, executes the exact query from Step 2, and exports the results to a file at `/home/user/anomalies.txt`.
   
   The output format in `/home/user/anomalies.txt` must strictly follow this structure for each row returned:
   `ALERT: [<sensor_id>] registered <temperature>C`
   *(Format the temperature to exactly 1 decimal place).*

4. **Execution**:
   - You may use `sudo apt-get install` to install `sqlite3` and `libsqlite3-dev` if needed.
   - Compile your C program to `/home/user/exporter` using `gcc /home/user/exporter.c -lsqlite3 -o /home/user/exporter`.
   - Run `/home/user/exporter` to generate the `/home/user/anomalies.txt` file.