You are an incident response log analyst. We have intercepted a batch of obfuscated log files and a proprietary, stripped binary tool (`/app/obfuscator_oracle`) that the attackers used to encode their logs. 

We need you to build a high-performance log ingestion service that decodes these logs and standardizes them into a queryable database. 

Here is your objective:
1. **Analyze the Binary**: The stripped binary `/app/obfuscator_oracle` takes a single obfuscated string as a command-line argument and prints the decoded, raw log line. You must either wrap this binary in a parallel processing pipeline or reverse-engineer its algorithm (which is highly recommended for performance) and reimplement it in Python.
2. **Create the Ingestion Service**: Write and run a Python HTTP server listening on `127.0.0.1:8000`. 
3. **Implement the Endpoint**: The server must expose a `POST /api/v1/ingest` endpoint. It will receive a JSON payload with the following structure:
   ```json
   {
     "batch_id": "some-uuid",
     "obfuscated_logs": [
       "obfuscated_string_1",
       "obfuscated_string_2",
       ...
     ]
   }
   ```
4. **Processing and Normalization**:
   - Decode each obfuscated log using the logic from the binary.
   - The decoded log will be a pipe-separated string: `TIMESTAMP|IPV4|SEVERITY|MESSAGE`.
   - Normalize the IP addresses (some might have leading zeros in octets, e.g., `192.168.001.001` -> `192.168.1.1`).
   - Standardize the SEVERITY to uppercase (e.g., `warn` -> `WARN`).
5. **Bulk Import**: 
   - Insert the normalized logs into an SQLite database located at `/home/user/logs.db`.
   - The table must be named `system_logs` with columns: `batch_id` (TEXT), `timestamp` (TEXT), `ip` (TEXT), `severity` (TEXT), `message` (TEXT).
   - Ensure you use bulk insertion for performance, as batches will contain up to 50,000 records.
6. **Response**: The endpoint should respond with HTTP 200 OK and a JSON body: `{"status": "success", "processed_count": N}`.

Start the service and leave it running in the background or foreground so it can be tested.