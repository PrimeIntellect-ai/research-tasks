You are an ETL data engineer working on processing security camera feeds that have embedded telemetry logs in their subtitle tracks. 

We have a video file located at `/app/security_feed.mp4`. The video contains a subtitle stream (SRT format) which captures JSON-formatted log lines dumped by the edge device.

Your task has two parts:

**Part 1: The Alert Formatter**
Write a Python script at `/home/user/format_alert.py` that acts as our core text-processing utility.
- It must read a single string from standard input (`stdin`).
- The expected string format is: `[LEVEL] {"field1": "value1", ...}`
  Example: `[CRITICAL] {"user": "sysadmin", "action": "auth_bypass", "ip": "192.168.1.50"}`
- The script must extract the log level and parse the JSON payload.
- It must generate a formatted text template to standard output (`stdout`) exactly as follows:
  ```
  ALERT LEVEL: <LEVEL>
  ACTION: <action>
  USER: <user>
  IP: <ip>
  ```
- If the input does not match the `[LEVEL] {json}` pattern, or if the JSON is malformed, or if any of the required keys (`user`, `action`, `ip`) are missing, the script must exactly output: `INVALID LOG` (with a trailing newline).

**Part 2: The ETL Pipeline**
1. Extract the subtitle track from `/app/security_feed.mp4`.
2. Filter the subtitle text to find only the lines that begin with `[` (ignoring SRT timestamp lines and sequence numbers).
3. Process every extracted log line through your `/home/user/format_alert.py` script.
4. Save the concatenated output of all valid alerts to `/home/user/extracted_alerts.txt`. Ensure there is a blank line between each alert block.

You may install any necessary packages using `apt` or `pip`. Ensure `/home/user/format_alert.py` is robust, as it will be rigorously tested against thousands of fuzzed variations in our CI pipeline.