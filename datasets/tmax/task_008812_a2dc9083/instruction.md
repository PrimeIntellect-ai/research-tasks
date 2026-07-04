You are a data analyst dealing with high-frequency server logs. To process these massive logs efficiently, you need to write a custom tool in C to extract information, detect changepoints (traffic anomalies), and load the results into an SQLite database for querying.

**Data Source:**
There is a log file located at `/home/user/server_logs.csv`.
It has no header. The columns are: `timestamp_sec,ip_address,endpoint,status_code,response_time_ms`.
The file is strictly ordered by `timestamp_sec`.

**Your Objective:**
1. **Write a C program (`/home/user/detector.c`):**
   - Parse `/home/user/server_logs.csv`.
   - Implement a tumbling (non-overlapping) window of **10 seconds** to count the number of requests per window.
   - The windows should start aligned to the nearest 10-second boundary based on the very first timestamp in the file. (e.g., if the first timestamp is 1000, windows are 1000-1009, 1010-1019, etc.).
   - **Anomaly Detection:** An anomaly is triggered in the current window $W_n$ if the total number of requests in $W_n$ is strictly greater than **3 times** the average number of requests of the strictly previous 5 windows ($W_{n-5}$ to $W_{n-1}$). 
   - Note: Anomalies cannot be triggered for the first 5 windows (there isn't enough history).
   - If a window is anomalous, extract *every unique IP address* that made a request during this window.
   - Output the results directly to `/home/user/anomalies.csv` in the format: `window_start_timestamp,ip_address,window_total_requests`. (One row per unique IP in the anomalous window, sorted alphabetically by IP address).

2. **Database Bulk Import:**
   - Create an SQLite database at `/home/user/alerts.db`.
   - Create a table named `anomalies` with the schema:
     `CREATE TABLE anomalies (window_start INTEGER, ip TEXT, count INTEGER);`
   - Bulk import the data from `/home/user/anomalies.csv` into this table. (You can use the `sqlite3` command-line tool which is already installed).

Compile your C program with `gcc -O2 /home/user/detector.c -o /home/user/detector` and run the end-to-end process. Ensure the final `/home/user/alerts.db` file is fully populated and accurately reflects the anomalous windows.