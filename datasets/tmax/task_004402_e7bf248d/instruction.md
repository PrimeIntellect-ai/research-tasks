You are a log analyst investigating a recent series of database poisoning attempts that occurred during specific network anomalies. You need to analyze a dashboard recording to find when the anomalies happened, build a robust Rust-based filter to sanitize logs from those times, and extract the clean data.

**Step 1: Video Analysis**
A dashboard recording is located at `/app/dashboard_recording.mp4` (10 seconds, 1 fps). An anomaly is indicated when the top-left corner (e.g., the 50x50 pixel region at 0,0) flashes pure red (RGB: 255, 0, 0).
Use `ffmpeg` or any suitable tool to analyze the video frames. Identify the exact seconds (0-9) where the red anomaly appears. 
Write these integer seconds to `/home/user/anomaly_seconds.txt`, one per line.

**Step 2: Adversarial Log Sanitizer (Rust)**
Attackers have been injecting malicious payloads into our logs. You must write a Rust program that reads text from `stdin`, filters out malicious lines, and prints only safe lines to `stdout`.
A line is considered "evil" (malicious) if it contains:
- SQL Injection vectors (e.g., `DROP TABLE`, `UNION SELECT` - case insensitive)
- Cross-Site Scripting vectors (e.g., `<script>`, `javascript:` - case insensitive)
- Terminal escape sequence injections (e.g., containing the `\x1B` or `\033` byte)

You are provided with two corpora for testing:
- `/app/corpora/clean/` (contains files with normal, safe log lines)
- `/app/corpora/evil/` (contains files where every line is a malicious payload)

Your Rust project should be created in `/home/user/sanitizer_project`. Compile it in release mode and place the final executable at `/home/user/bin/sanitizer`. Your program will act as a Validation Checkpoint / Quality Gate. It MUST preserve 100% of the lines from the clean corpus and reject (drop) 100% of the lines from the evil corpus.

**Step 3: Database Extraction and Pipeline Integration**
We have a bulk SQLite database at `/app/raw_logs.db` containing a table `logs(id INTEGER, timestamp_sec INTEGER, message TEXT)`.
1. Bulk export the `message` field for all rows where the `timestamp_sec` exactly matches one of the anomaly seconds you found in Step 1.
2. Pipe these exported messages through your Rust sanitizer (`/home/user/bin/sanitizer`).
3. Save the resulting clean, sanitized messages to `/home/user/sanitized_anomalies.txt`.

**Step 4: Scheduling**
Create a cron job configuration file at `/home/user/pipeline.cron` that schedules a script named `/home/user/run_pipeline.sh` to run exactly every 15 minutes. (You do not need to write the `run_pipeline.sh` script, just the cron schedule file).