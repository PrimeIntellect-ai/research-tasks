You are a storage administrator responsible for managing disk space and fixing a broken automated backup system. Recently, the system ran out of disk space because the backup script blindly followed symlinks into infinite loops. You need to perform several cleanup and diagnostic tasks using Bash.

**Stage 1: Video Analysis**
A monitoring system recorded the server dashboard during the failure event. The video is located at `/app/dashboard_alert.mp4`.
Whenever the storage array hit a critical I/O block, the dashboard flashed a solid, bright red frame (pure RGB #FF0000). 
Write a script to extract the frames from this video using `ffmpeg` and count the exact number of solid red frames. Save this integer count to `/home/user/red_frame_count.txt`.

**Stage 2: Backup Target Sanitizer**
The backup system needs a filter to prevent archiving directories that contain symlink loops or recursive symlink chains. 
Write a Bash script at `/home/user/sanitizer.sh` that takes a single directory path as an argument.
- It must exit with code 0 (Accept) if the directory is completely safe (contains no symlink loops or broken recursive links).
- It must exit with code 1 (Reject) if the directory or any of its subdirectories contain a symlink loop.
Your script will be tested against a hidden corpus of clean and malicious directory structures to ensure it perfectly identifies symlink loops without false positives.

**Stage 3: Multi-line Log Parsing & Manifest Generation**
The backup system generated a massive log file at `/app/backup_runs.log`. The log entries are multi-line, formatted as follows:
```
[Timestamp]
Target: /path/to/some/dir
Owner: username
Status: [SUCCESS|FAILED|IN_PROGRESS]
Bytes: 1024
--
```
You need to parse this log file and find all `Target` directories where the `Status` was exactly `FAILED`.
For each failed target directory that actually exists on the filesystem (under `/app/staging/`), use metadata-based file search to find all `.dat` files within those directories that were modified in the last 7 days.
Generate a SHA-256 checksum manifest of these specific `.dat` files and save it to `/home/user/failed_dat_manifest.txt`. The manifest must be in standard `sha256sum` output format (checksum followed by two spaces and the absolute file path), sorted alphabetically by file path.

Ensure your `sanitizer.sh` is robust, as it will be subjected to an automated test suite.