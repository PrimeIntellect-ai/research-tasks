You are a data engineer tasked with building an ETL extraction tool in C for a legacy system. 

You have been provided with an undocumented SQLite database file located at `/home/user/data/legacy_telemetry.db`. 

Your objectives are:
1. **Reverse Engineer the Schema:** Inspect the database to understand the tables and their columns. There is a single table containing telemetry events (with columns for a unique ID, a device identifier, a timestamp, and a sensor reading). 
2. **Install Dependencies:** You may need to install standard development libraries for SQLite3 to write and compile C code against it.
3. **Write the Extractor:** Create a C program at `/home/user/pipeline/extractor.c`. This program must:
   - Take exactly two command-line arguments: the path to the database, and a floating-point threshold value. (e.g., `./extractor /home/user/data/legacy_telemetry.db 45.5`)
   - Connect to the SQLite database.
   - Execute a query using **parameter binding** (do not use string concatenation for the threshold parameter to prevent SQL injection).
   - The query must calculate a 3-row moving average (the current row and the 2 preceding rows) of the sensor reading. The moving average must be partitioned by the device identifier and ordered by the timestamp in ascending order.
   - Use a Common Table Expression (CTE) or subquery to filter the final results, returning ONLY rows where the calculated 3-row moving average is strictly greater than the threshold parameter provided via the command line.
   - Write the filtered results to `/home/user/pipeline/alerts.csv`.
4. **Output Format:** The output CSV must have a header row: `device,timestamp,reading,moving_average`. Subsequent rows must format the `reading` and `moving_average` to exactly 2 decimal places.
5. **Compile and Run:** Compile your code into an executable named `/home/user/pipeline/extractor` and run it with a threshold of `50.00`.

Make sure `/home/user/pipeline/alerts.csv` exactly reflects the results of running the executable with the `50.00` threshold.