You are a log analyst investigating a potential security incident. You have been provided with a raw log file `/home/user/logs.csv` and a proprietary binary tool `/app/log_distance`.

Your objective is to build a data processing pipeline and expose its results via a REST API.

1. **Log Processing Pipeline**:
   The log file `/home/user/logs.csv` contains thousands of entries with the following columns: `raw_timestamp`, `user_ip`, `action`, `details`.
   You must process this file to:
   - **Timestamp Alignment**: Parse `raw_timestamp` (which varies between Unix epoch integers and `MM/DD/YYYY HH:MM:SS` formats) and convert it to strict ISO8601 UTC format (`YYYY-MM-DDTHH:MM:SSZ`).
   - **Data Masking**: Anonymize the `user_ip` field by replacing all IPv4 octets with `X` (e.g., `192.168.1.50` becomes `X.X.X.X`).
   - **Similarity Computation**: Use the provided stripped binary `/app/log_distance`. This tool calculates the behavioral distance between a log's `details` string and a known malicious signature. You must invoke it as: `/app/log_distance "known malicious payload signature" "<details_string>"`. It outputs a float representing the distance (lower means more similar). 
   Use `"root shell attempt"` as the exact reference signature for the first argument.

2. **Web Service (multi-protocol)**:
   Write a server (you may use Bash with `socat`/`nc` or Python) that listens on `127.0.0.1:8080`.
   - Protocol: HTTP GET
   - Endpoint: `/api/anomalies?max_distance=<float>`
   - Behavior: When the endpoint is queried, your server must return a JSON response containing an array of all processed log entries where the calculated distance is less than or equal to `max_distance`.
   - The JSON output should look like this:
     ```json
     [
       {
         "timestamp": "2023-10-04T12:00:00Z",
         "ip": "X.X.X.X",
         "action": "login",
         "distance": 0.42
       }
     ]
     ```
   - Sort the output array chronologically by `timestamp` in ascending order.

Start the service in the background and ensure it is fully functional. Do not include any authentication.