You are a log analyst investigating a sophisticated botnet attack on a global server infrastructure. You have access to server logs and a screen recording of the security dashboard. 

Your objective is to build a robust log sanitizer pipeline that filters out bot-generated and attack-window traffic based on visual cues, time-series analysis, and Unicode anomalies.

**1. Video Analysis**
You are provided with a video of the security dashboard at `/app/dashboard.mp4`. 
- The video framerate is exactly 1 FPS and it is 120 seconds long.
- The video recording started at exactly UNIX epoch time `1710000000` (this corresponds to the first frame at `t=0`).
- During active DDoS attack windows, a red warning indicator flashes in the top-left corner. Specifically, the average Red channel value in the top-left 10x10 pixel block exceeds 200 (while Green and Blue remain < 50).
- **Task:** Extract the exact UNIX epoch seconds where the attack indicator is active.

**2. Log Sanitization Pipeline**
Write a Python script at `/home/user/sanitizer.py` that processes raw log files.
Your script must be callable exactly as follows:
`python3 /home/user/sanitizer.py --input_dir <INPUT_DIR> --output_dir <OUTPUT_DIR>`

The script must read all `.log` files in `<INPUT_DIR>` and write the cleaned versions to `<OUTPUT_DIR>` maintaining the exact same filenames.

**Log Format:**
Logs are UTF-8 encoded plain text. Each line is formatted as:
`UNIX_TIMESTAMP_MS | USER_ID | LOG_MESSAGE`
*(Note: The timestamp is in milliseconds. `USER_ID` is an alphanumeric string. `LOG_MESSAGE` is a space-separated text string).*

**Filtering Rules:**
A log line MUST BE DROPPED (filtered out) if it meets **ANY** of the following three criteria:

1. **Attack Window (Video Integration):** The log's timestamp (converted to a truncated integer UNIX epoch second) matches one of the active attack seconds extracted from the video.
2. **Rolling Time-Series Anomaly:** The botnet generates requests at highly mechanical intervals. If the `USER_ID`'s last 5 requests (including the current request) have a **sample standard deviation** (N-1) of inter-arrival times (differences between consecutive request timestamps in milliseconds) of **less than 100.0 ms**, drop the current request. *(Note: A user must have at least 5 requests before this rule can trigger).*
3. **Unicode Homoglyph Attack:** The `LOG_MESSAGE` contains at least one space-separated word that mixes Latin alphabet characters (A-Z, a-z) and Cyrillic alphabet characters (А-Я, а-я, Ё, ё) within the exact same word.

Any log line that does not trigger the above rules must be preserved exactly as it was in the output file.