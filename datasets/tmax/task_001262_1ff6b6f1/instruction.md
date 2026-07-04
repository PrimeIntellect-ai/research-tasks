You are an operations engineer tasked with building a robust HTTP server in Python to handle video event logging and secure archiving. You must handle concurrent logging safely and package the data alongside a surveillance video.

A video file is located at `/app/surveillance.mp4`. 

Write a Python web server (you may install and use `Flask` or `FastAPI` via pip, or use the standard library) that listens on `127.0.0.1:8080`. The server must implement the following endpoints:

1. `POST /analyze`
   - Analyzes `/app/surveillance.mp4` (using `ffmpeg`/`ffprobe` which are preinstalled) to determine the exact total number of frames in the video.
   - Securely acquires an exclusive file lock (using `fcntl`) on `/tmp/video_events.jsonl` and appends a JSON line: `{"timestamp": "0", "event": "Video contains X frames"}` where X is the exact frame count.
   - Returns a 200 OK HTTP status.

2. `POST /log`
   - Accepts a JSON payload with the format `{"timestamp": "<str>", "event": "<str>"}`.
   - Safely appends this exact JSON object as a new line to `/tmp/video_events.jsonl`.
   - You MUST use exclusive file locking (e.g., `fcntl.flock`) during the file write to prevent data corruption from concurrent requests.
   - Returns a 200 OK HTTP status.

3. `GET /backup`
   - Securely acquires an exclusive lock on `/tmp/video_events.jsonl`.
   - Converts the contents of `/tmp/video_events.jsonl` into a CSV file at `/tmp/video_events.csv` with headers `timestamp` and `event`.
   - Creates a ZIP archive at `/tmp/backup.zip` containing both `/tmp/video_events.csv` (at the root of the zip) and the original video file `/app/surveillance.mp4` (at the root of the zip, named `surveillance.mp4`).
   - Verifies the integrity of the created ZIP archive programmatically (e.g., using Python's `zipfile` module to ensure it is not corrupt).
   - If the archive is valid, returns the ZIP file in the HTTP response body with the appropriate content type (`application/zip`). If invalid, returns a 500 status.

Start your server in the background so it remains running. The verification script will send concurrent requests to your server to test the file locking, trigger the video analysis, and finally download and inspect the backup archive.