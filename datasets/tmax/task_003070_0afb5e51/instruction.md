You are an automation specialist tasked with creating a robust data ingestion workflow. We have a legacy system that exposes application logs via an HTTP endpoint. The logs suffer from intermittent timestamp drops, mixed character encodings, and inconsistent Unicode normalizations.

Your objective is to write a Go program that retrieves this log file, normalizes the data, interpolates missing timestamps, and outputs a clean JSONL (JSON Lines) file.

**Environment & Setup:**
A local HTTP server is running at `http://127.0.0.1:8080` and serves the raw log file at `http://127.0.0.1:8080/raw.log`. 
*(Note: If the server isn't running, you may assume it's a simulated environment, but for this task, write your code to fetch from this URL).*

**Input Data Format:**
The file contains plain text lines in the following format:
`[TIMESTAMP] MESSAGE_CONTENT`
- `TIMESTAMP` is an ISO-8601 formatted string (e.g., `2023-10-01T12:00:00.000Z`), OR it is exactly `???` indicating a missing timestamp.
- `MESSAGE_CONTENT` is the rest of the line.

**Processing Requirements:**
1. **Fetch:** Your Go program must download the log data from `http://127.0.0.1:8080/raw.log`.
2. **Character Encoding:** The legacy system sometimes outputs invalid UTF-8 bytes (specifically, Windows-1252 encoding). For each message, if the byte sequence is not valid UTF-8, decode it as Windows-1252 (Code Page 1252) to UTF-8. 
3. **Unicode Normalization:** Regardless of the original encoding, all `MESSAGE_CONTENT` must be standardized to Unicode Normalization Form C (NFC).
4. **Gap-Filling (Interpolation):** Missing timestamps (`???`) must be linearly interpolated based on the nearest surrounding valid timestamps. 
   - For example, if there is a gap of two missing timestamps between `2023-10-01T12:00:00.000Z` and `2023-10-01T12:00:03.000Z`, the missing ones should be assigned `2023-10-01T12:00:01.000Z` and `2023-10-01T12:00:02.000Z`.
   - You can assume the first and last lines of the log will always have valid timestamps.
   - Interpolated timestamps must be formatted back to RFC3339/ISO-8601 with millisecond precision (e.g., `2023-10-01T12:00:01.000Z`).
5. **Output:** Write the processed data to `/home/user/processed_logs.jsonl`. Each line must be a valid JSON object with exactly two keys:
   `{"timestamp": "...", "message": "..."}`

**Constraints:**
- Use Go to implement this solution. You should initialize a Go module in `/home/user/log_processor` (e.g., `go mod init log_processor`).
- You may use standard libraries and `golang.org/x/text`.
- The final output file must exactly match the expected normalizations and interpolated timestamps.

Please create and execute this Go program to generate `/home/user/processed_logs.jsonl`.