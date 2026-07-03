You are an edge computing engineer deploying a new alerting system to an IoT device. You must configure the environment, analyze a sample video feed from the edge camera, and implement a high-performance C log processor that determines when to trigger email alerts based on scheduled configurations.

Perform the following tasks:

1. **Environment Setup**
   The device needs specific environment variables for locale and identity. Add the following exports to `/home/user/.bash_profile`:
   - `TZ=Pacific/Honolulu`
   - `DEVICE_ID=CAM_EDGE_01`

2. **System Config File**
   Create a configuration file at `/home/user/edge.conf` with the following key-value pairs (one per line):
   ```
   THRESHOLD=80
   ADMIN_EMAIL=admin@iot.local
   ```

3. **Video Feed Analysis**
   A sample video feed from the camera is located at `/app/iot_feed.mp4`. Due to sensor glitches, the camera occasionally records completely black frames (RGB 0,0,0). 
   Use `ffmpeg` or any suitable tool to analyze this video. Find the 0-indexed frame numbers of all completely black frames.
   Write these frame numbers (one per line) to `/home/user/glitch_frames.txt`.

4. **C Log Processor Implementation**
   Write a C program at `/home/user/log_processor.c` and compile it to `/home/user/log_processor`. This program will act as our fast data filter.
   It must do the following:
   - Read the `DEVICE_ID` from the environment. (If missing, default to `UNKNOWN`).
   - Parse `/home/user/edge.conf` to extract `THRESHOLD` (integer) and `ADMIN_EMAIL` (string).
   - Read line-by-line from standard input (`stdin`). Each line contains a UNIX timestamp and a sensor reading: `<UNIX_TIMESTAMP> <VALUE>` (e.g., `1716300000 85`).
   - For each line, convert the timestamp to a local time string (respecting the `TZ` environment variable you set, formatted as `YYYY-MM-DD HH:MM:SS`).
   - Evaluate the reading against the threshold:
     - If `VALUE >= THRESHOLD`, print to `stdout`: 
       `[DEVICE_ID] YYYY-MM-DD HH:MM:SS - ALERT: VALUE >= THRESHOLD. Emailing ADMIN_EMAIL`
     - If `VALUE < THRESHOLD`, print to `stdout`:
       `[DEVICE_ID] YYYY-MM-DD HH:MM:SS - OK: VALUE`
     *(Replace `DEVICE_ID`, `YYYY-MM-DD HH:MM:SS`, `VALUE`, `THRESHOLD`, and `ADMIN_EMAIL` with the actual values.)*

5. **Scheduled Task Setup**
   We need to schedule the log processing. Create a cron configuration file at `/home/user/edge_cron` that specifies a job to run every 15 minutes. The job command should be:
   `/home/user/log_processor < /var/log/sensor.log >> /var/log/processed.log`