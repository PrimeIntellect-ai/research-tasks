You are a data analyst managing a pipeline that ingests CSV log files associated with a continuous video feed. Recently, corrupted and maliciously malformed logs have been polluting our large-scale data storage.

We have a reference video file located at `/app/data/conveyor.mp4`. 
We also have a set of test logs in `/app/corpora/clean/` (which are entirely valid) and `/app/corpora/evil/` (which contain various corruptions).

Your task is to create a robust, reproducible data validation pipeline in Bash. Specifically, write a bash script at `/home/user/validate_logs.sh` that takes a single CSV file path as its argument. The script must exit with status `0` if the CSV is completely valid, and exit with status `1` (or any non-zero value) if the CSV violates any of the rules below.

Rules for a valid CSV:
1. **Row Count Match**: The CSV must have exactly one header row followed by exactly `N` data rows, where `N` is the exact number of frames in the video `/app/data/conveyor.mp4`. You may use `ffmpeg` or `ffprobe` to determine the frame count.
2. **Header**: The first line must be exactly `frame,timestamp_sec,event_code`.
3. **Sequential Frames**: The `frame` column must start at `1` and increment by exactly `1` for each subsequent row.
4. **Monotonic Timestamps**: The `timestamp_sec` column (floating point numbers) must be strictly increasing.
5. **Valid Event Codes**: The `event_code` column must be a valid 4-digit uppercase hexadecimal string prefixed with `0x` (e.g., `0x0000`, `0x1A2F`, `0xFFFF`).

Requirements:
- Write the script strictly in Bash (you can use standard CLI tools like `awk`, `sed`, `grep`, `ffprobe`).
- The script must be executable.
- The script should not produce any standard output or standard error that would break the pipeline; it only needs to exit with the correct status.
- You must ensure the script accurately rejects 100% of the evil corpus while preserving 100% of the clean corpus.