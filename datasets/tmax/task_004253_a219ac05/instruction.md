A critical server experienced a catastrophic failure. The logging daemon crashed prior to the incident, and the only surviving record of the system's final moments is a low-framerate screen recording of the console monitor captured by an external security camera. 

You are stepping in as the lead log analyst to investigate the patterns that led to the crash. You need to extract the raw text from the video, normalize it, and prepare it for remote ingestion.

The video file is located at: `/app/incident_044.mp4`

Your objective is to build a Python pipeline that performs the following steps:
1. Extracts the frames from the video.
2. Uses Tesseract OCR (available via the `pytesseract` Python library or `tesseract` CLI) to read the text from the terminal screen in the video.
3. Cleans and deduplicates the scrolling text. Because it's a video of a scrolling terminal, many frames will capture overlapping or identical log lines. You must consolidate these into a single, continuous, chronologically ordered sequence of log events.
4. Tokenizes and normalizes the log lines into a structured JSON Lines (`.jsonl`) format. 
5. Outputs the final structured logs to `/home/user/reconstructed_logs.jsonl`.

Each line in `/home/user/reconstructed_logs.jsonl` must be a valid JSON object with the following keys:
- `timestamp`: The timestamp string exactly as it appears in the log.
- `level`: The severity level extracted from the log (e.g., INFO, WARN, ERROR, FATAL).
- `message`: The rest of the log message text, stripped of leading/trailing whitespace.

Example output line:
`{"timestamp": "2024-10-12T08:33:01Z", "level": "ERROR", "message": "Connection timeout on port 8080"}`

Be sure to handle OCR artifacts and typos gracefully. An automated evaluator will parse your `/home/user/reconstructed_logs.jsonl` and compare the sequence of messages against the known ground-truth logs using a string similarity metric. You must achieve a similarity score of at least 85% to succeed.