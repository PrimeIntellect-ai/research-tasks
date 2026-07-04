You are a log analyst investigating a new set of error patterns on your web servers. You need to extract specific error traces from a messy log file, normalize the data, deduplicate the errors, and push the processed data to a local SIEM ingestion endpoint.

We have a raw log file located at `/home/user/raw_server.log`.

Your task is to write and execute a Go program at `/home/user/process_logs.go` that does the following:

1. **Regex Parsing:** Read `/home/user/raw_server.log` and extract all log lines that represent an error with a specific code format. The target lines contain the word `ERROR`, followed by a space, followed by an error code enclosed in brackets like `[CODE-XXXX]` (where X is exactly 4 digits), followed by a space, and then the error message. 
   
2. **Cleaning and Normalization:** 
   - The log file contains timestamps at the beginning of each line enclosed in brackets. There are two timestamp formats mixed in the logs:
     Format A: `[YYYY/MM/DD HH:MM:SS]` (e.g., `[2023/10/12 08:14:02]`). Assume these are in UTC.
     Format B: `[DD MMM YY HH:MM:SS MST]` (e.g., `[12 Oct 23 08:15:00 UTC]`).
   - Parse these timestamps and normalize them to the standard RFC3339 format (e.g., `2023-10-12T08:15:00Z`).
   
3. **Deduplication:** If multiple errors have the exact same 4-digit code (e.g., `CODE-1052`), only keep the **first** occurrence (chronologically as they appear top-to-bottom in the file) and discard the rest.

4. **Formatting:** Structure the deduplicated and normalized errors into a JSON array of objects. Each object must have exactly these keys:
   - `"timestamp"`: The normalized RFC3339 timestamp string.
   - `"code"`: The exact 4-digit code string (e.g., `"1052"`).
   - `"message"`: The rest of the log message after the code bracket.

5. **Local-Remote Transfer:** Have your Go program perform an HTTP POST request containing the JSON payload to the local SIEM mock endpoint running at `http://localhost:8080/ingest`. Ensure the `Content-Type` header is set to `application/json`.

The mock SIEM server is already running in your environment. Once your Go script completes successfully, the SIEM server will save your payload to `/home/user/siem_ingest.json`.