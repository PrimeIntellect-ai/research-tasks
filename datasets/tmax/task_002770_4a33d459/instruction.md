You are a log analyst investigating a potential data exfiltration incident. We have intercepted a large traffic log file and a suspicious audio recording from the attacker's communication channel. 

Your objective is to extract the target IP from the audio recording, process the massive log file to extract time-series metrics for that IP, reshape the data, and serve the final report via a live HTTP server so our automated forensics tool can ingest it.

**Step 1: Audio Analysis**
We found an audio file at `/app/incident_comms.wav`. It contains a short voice memo from the attacker stating the target IP address they were focusing on. Transcribe this audio (you may install and use Python libraries like `openai-whisper` or `SpeechRecognition`) to recover the IP address.

**Step 2: Log Processing & Extraction**
You have a large, mixed-encoding log file at `/app/raw_traffic_logs.txt`. The file contains unstructured text logs. 
- You must stream-process this file to avoid running out of memory. 
- Handle character encoding gracefully (some lines are UTF-8, some are Windows-1252; ignore or replace invalid characters).
- Extract the following from each line: the ISO8601 Timestamp, the Source IP, and the `bytes_transferred` value. The logs look generally like: `[TIMESTAMP] Connection from IP: <IP> - payload size: <bytes_transferred> bytes`.

**Step 3: Time-Series Reshaping**
Filter the extracted records to ONLY include the target IP you identified from the audio file.
Aggregate the `bytes_transferred` for this IP by the **hour** (e.g., `2023-10-04T08`, `2023-10-04T09`).
Reshape this data from a long format into a wide format (dictionary), where the keys are the Hour strings and the values are the total bytes transferred in that hour.

**Step 4: Template-based Generation & Serving**
Create a Python HTTP server (e.g., using `http.server` or `Flask`/`FastAPI`) listening on `127.0.0.1:8333`.
When a `GET` request is made to `/exfiltration-report`, the server must return a 200 OK response with a JSON payload strictly matching this template:
```json
{
  "investigator": "log-analyst-1",
  "target_ip": "<EXTRACTED_IP>",
  "hourly_exfiltration": {
    "<HOUR_1>": <TOTAL_BYTES>,
    "<HOUR_2>": <TOTAL_BYTES>
  }
}
```

Ensure the server remains running in the foreground or background so it can be queried. Notify when the server is ready.