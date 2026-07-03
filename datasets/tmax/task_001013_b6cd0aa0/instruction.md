You are an automation specialist building a log ingestion workflow. We have a legacy system that generates logs with highly inconsistent timestamp formats and unstructured text. I need you to write a Go program to parse these logs, filter for specific alert events, align the timestamps, and output a clean JSON Lines (JSONL) file for our monitoring pipeline.

The raw log file is located at `/home/user/legacy.log`.

Your task:
Write a Go script at `/home/user/parser.go` that reads `/home/user/legacy.log` and does the following:
1. **Filtering & Regex Extraction:** Only process lines that contain an `ERROR` or `WARN` log level AND are associated with a user ID matching the exact pattern `[USR-<digits>]` (e.g., `[USR-123]`). Ignore `INFO` logs or alerts triggered by non-user entities (like `[SYS-001]`).
2. **Timestamp Alignment:** Extract the timestamp at the beginning of the line. The legacy system outputs timestamps in one of three messy formats:
   - `YYYY/MM/DD-HH:MM:SS` (e.g., `2023/10/24-14:23:10`)
   - `MM-DD-YYYY HH:MM:SS` (e.g., `10-24-2023 14:25:01`)
   - `YYYY.MM.DD HH:MM:SS` (e.g., `2023.10.24 14:26:15`)
   Parse the matched timestamp and convert it into standard RFC3339 format (assume UTC for all times).
3. **Structured Output:** For every matched line, write a JSON object to `/home/user/normalized_alerts.jsonl`. Each JSON object must have exactly these keys:
   - `"time"`: The RFC3339 formatted timestamp.
   - `"level"`: The extracted log level (`ERROR` or `WARN`).
   - `"user"`: The extracted user ID (e.g., `USR-123`, without the brackets).
   - `"msg"`: The remaining log message text after the user ID, with leading/trailing whitespace removed.

Example line:
`10-24-2023 14:25:01 ERROR [USR-099] Connection timeout in region us-east.`
Should become:
`{"time":"2023-10-24T14:25:01Z","level":"ERROR","user":"USR-099","msg":"Connection timeout in region us-east."}`

After writing your Go script, run it to generate the `/home/user/normalized_alerts.jsonl` file.