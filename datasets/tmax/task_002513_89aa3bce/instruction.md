As a database administrator, you need to build a C utility to analyze server metrics from an SQLite database. We have a database located at `/home/user/metrics.db` containing a table `server_metrics` with the following schema:
`CREATE TABLE server_metrics (server_id TEXT, timestamp INTEGER, cpu_usage REAL);`

Your task is to create a C program at `/home/user/analyze_metrics.c` that identifies anomalous CPU usage spikes. 

The program must:
1. Accept two command-line arguments: a `server_id` (string) and a `threshold_multiplier` (float).
2. Connect to `/home/user/metrics.db` using the SQLite C API.
3. Execute a parameterized query (you MUST use `sqlite3_prepare_v2` and `sqlite3_bind_*` functions to prevent SQL injection and optimize query planning).
4. The query must calculate a rolling moving average of `cpu_usage` for the specified `server_id`. The moving average should be calculated over a window consisting of the current row and the 2 strictly preceding rows, ordered by `timestamp` ascending.
5. The query should return only the rows where the actual `cpu_usage` is strictly greater than the calculated moving average multiplied by the `threshold_multiplier`.
6. Write the results to `/home/user/anomalies.log`.

For each matching row, append a line to `/home/user/anomalies.log` in exactly this format:
`Server: <server_id>, TS: <timestamp>, CPU: <cpu_usage>, MA: <moving_avg>`
(Format the floating point numbers to exactly 2 decimal places).

Example execution:
`gcc /home/user/analyze_metrics.c -o /home/user/analyze_metrics -lsqlite3`
`/home/user/analyze_metrics "server_A" 1.5`

Ensure your C program handles standard SQLite return codes and cleans up resources properly. Compile the program to an executable named `/home/user/analyze_metrics` and run it with `server_A` and `1.5` as arguments to generate the final log file.