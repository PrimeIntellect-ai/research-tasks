You are a data scientist tasked with cleaning a large dataset of legacy sensor logs. The data is currently obfuscated and stored in a large file. You must decode, clean, and summarize the data, and finally serve the results over a simple HTTP server written purely in Bash.

Here are the specific requirements:

1. **Data Decoding**:
   - You are provided with a large obfuscated file at `/home/user/raw_sensor_logs.txt`.
   - There is a stripped legacy binary located at `/app/legacy_decoder`.
   - The binary reads obfuscated lines from standard input and outputs decoded comma-separated values (CSV) in the format: `timestamp,sensor_id,reading_value`.
   - Stream the contents of `/home/user/raw_sensor_logs.txt` through `/app/legacy_decoder`.

2. **Data Cleaning & Normalization**:
   Process the decoded stream using purely standard Linux CLI tools (awk, sed, sort, uniq, etc.) to produce a file at `/home/user/cleaned_data.csv` satisfying these rules:
   - Drop any rows where `reading_value` is less than 0 or the string is exactly "ERROR".
   - Normalize the `sensor_id` column to be strictly uppercase.
   - Deduplicate the dataset (remove rows that are exactly identical).
   - Sort the final output chronologically by `timestamp` (ascending).

3. **Template-Based Report Generation**:
   Generate an HTML summary report at `/home/user/report.html` matching exactly this template format:
   ```html
   <html>
   <body>
   <h1>Sensor Data Report</h1>
   <p>Total Cleaned Records: [COUNT]</p>
   <p>Unique Sensors: [SENSOR_COUNT]</p>
   </body>
   </html>
   ```
   Replace `[COUNT]` with the number of rows in `cleaned_data.csv`, and `[SENSOR_COUNT]` with the number of distinctly unique `sensor_id`s present in the cleaned data.

4. **HTTP Serving (Bash-only)**:
   - Write and start a Bash script at `/home/user/server.sh` that acts as a simple HTTP server listening on `127.0.0.1:9090`.
   - You must use `nc` (netcat) or `socat` within a loop in the script. Do not use Python, Node, or other high-level languages.
   - If a client issues an HTTP `GET /cleaned_data.csv HTTP/1.1` request, the server must respond with a valid HTTP 200 OK header followed by the contents of `/home/user/cleaned_data.csv`.
   - If a client issues an HTTP `GET /report.html HTTP/1.1` request, the server must respond with a valid HTTP 200 OK header followed by the contents of `/home/user/report.html`.
   - Leave the server running in the background.

Please complete all steps using Bash built-ins and standard coreutils.