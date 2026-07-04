You are tasked with building a backup and archiving agent that handles a live-rotating log stream and video metadata. You must process a video fixture, set up an HTTP API to trigger backups, and implement an incremental read mechanism that safely races with log rotation.

**Step 1: Video Metadata Extraction**
You have been provided a surveillance video file at `/app/evidence.mp4`.
Using `ffprobe`, extract the timestamps of all video frames that are "I-frames" (keyframes).
Save these timestamps as a single-column CSV file at `/home/user/frames.csv` (one timestamp per line, no header).
Count the total number of I-frames found.

**Step 2: Incremental Backup Service**
Write and run a Python HTTP server listening on `0.0.0.0:8333`. This service must manage incremental backups of a JSONL log file located at `/app/live_logs/active.jsonl`.

The log writer (an external process) will periodically append JSON objects to `/app/live_logs/active.jsonl`. Occasionally, it will rotate the log by renaming it to `/app/live_logs/active.jsonl.1` and creating a new `/app/live_logs/active.jsonl`.

Your Python service must implement two endpoints:

1. **`POST /backup`**
   - When called, the service must perform an incremental read of the log files.
   - It must track inodes or file sizes to detect if rotation occurred since the last backup. If a rotation happened, it must read any unread lines from `/app/live_logs/active.jsonl.1` before reading the new `/app/live_logs/active.jsonl`.
   - It must take all *new* JSONL lines found during this backup run, save them to a temporary file, and then create a compressed archive containing these new log lines and the `/home/user/frames.csv` file.
   - You must use standard stream redirection via Python's `subprocess` module to create the archive (e.g., piping `tar` to `gzip`). Save the archive to `/home/user/archive/backup_<N>.tar.gz` (where N increments from 1).
   - Return a `200 OK` response when finished.

2. **`GET /stats`**
   - Return a JSON response with exactly this schema:
     `{"total_backed_up_lines": <integer>, "total_keyframes": <integer>}`
   - `total_backed_up_lines` is the cumulative number of log lines your service has successfully read and archived across all `/backup` calls.
   - `total_keyframes` is the integer count of I-frames you extracted in Step 1.

**Requirements & Constraints:**
- The primary logic must be in Python.
- Create all necessary destination directories (like `/home/user/archive/`) before the service receives requests.
- Leave the service running in the foreground or background so the verification suite can interact with it.