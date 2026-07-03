You are acting as a technical compliance officer. We have received an automated audio log of an incident report and a snapshot of our system's access database. You need to identify unauthorized server access events related to the server mentioned in the audio log.

Your tasks are to:
1. **Transcribe the Audio:** Analyze the audio file located at `/app/audit_recording.wav`. It contains a short, spoken incident report that explicitly names a target server (e.g., "SERVER-XYZ"). You may install and use any tools (like `ffmpeg` or download `whisper.cpp`) to transcribe it.
2. **Data Extraction & Index Repair:** We have an SQLite database at `/app/compliance.db`. It contains two tables:
   - `access_logs (id INTEGER, server_name TEXT, user_id TEXT, timestamp INTEGER)`: Contains raw access logs. **Warning:** Our DB admins reported that a recent migration corrupted the index on `server_name` in this table, causing standard indexed queries to return stale or missing rows. You must bypass or fix this index to get accurate results.
   - `kg_edges (subject TEXT, predicate TEXT, object TEXT)`: A knowledge graph representing system permissions. An edge `(user_id, 'CAN_ACCESS', server_name)` means the user is authorized.
3. **Graph Pattern Matching:** For every access event in `access_logs` matching the transcribed server name, check if a corresponding authorization edge exists in `kg_edges`. 
4. **Aggregation & Export:** Write a Go program at `/home/user/audit.go` (and run it) that performs this data retrieval, cross-query validation, and exports the unauthorized access events to `/home/user/report.json`.
5. **Output Schema:** The output `/home/user/report.json` must strictly follow this JSON schema:
   ```json
   {
     "server_audited": "EXTRACTED_SERVER_NAME",
     "unauthorized_access": [
       {
         "user_id": "string",
         "timestamp": 1234567890
       }
     ]
   }
   ```

Write and execute the Go code to process the data, perform the checks, and generate the final JSON report.