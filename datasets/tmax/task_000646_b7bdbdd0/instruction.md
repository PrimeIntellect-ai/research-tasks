You are an automation specialist setting up a real-time anomaly detection workflow for time-series logs. 

We receive streaming JSON-lines from a legacy system over TCP, but the payload messages contain Unicode escape sequences (e.g., `\u0021` for `!`). We have an existing, proprietary anomaly scoring engine provided as a stripped binary at `/app/legacy_analyzer`. Unfortunately, if this binary encounters raw JSON or unescaped Unicode sequences, it either crashes or produces wildly inaccurate anomaly scores.

Your task is to write a C program that acts as a middleware stream processor. 

Here are the requirements for your C program:
1. **Network Service:** Listen for incoming TCP connections on `127.0.0.1` port `8888`.
2. **Stream Processing:** Read incoming data line by line. Each line will be a JSON object like:
   `{"ts": "2023-10-01T12:00:00Z", "msg": "System operational\u0021"}`
3. **Extraction & Parsing:** 
   - Extract the ISO8601 timestamp from the `ts` field and convert it to a UNIX epoch integer.
   - Extract the string from the `msg` field.
4. **Data Normalization:** Decode any `\uXXXX` unicode escape sequences in the `msg` string into standard ASCII/UTF-8 characters (you can assume all escaped characters will fall into the standard printable ASCII range after decoding).
5. **Anomaly Detection:** For each parsed line, feed the fully decoded `msg` string to the standard input (stdin) of the `/app/legacy_analyzer` binary, and read the resulting integer score from its standard output (stdout).
6. **Output:** For each processed line, write a CSV-formatted line back to the TCP client in the exact format: `<unix_epoch_timestamp>,<anomaly_score>\n`

Example input over TCP:
`{"ts": "2023-11-15T08:30:00Z", "msg": "High CPU load on db-node-01\u002e"}`

Example expected output returned over TCP (assuming the analyzer returns `85` for "High CPU load on db-node-01."):
`1700037000,85`

Write your C code to `/home/user/stream_processor.c`. Compile it using standard `gcc` without requiring any external build systems or third-party libraries (standard POSIX C libraries are fine). Run your compiled server in the background so it is actively listening on port 8888. Do not stop the server once it is running.