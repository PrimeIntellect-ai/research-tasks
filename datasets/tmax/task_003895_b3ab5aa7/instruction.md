You are a deployment engineer tasked with rolling out an update to our edge camera monitoring pipeline. You need to prepare the deployment, analyze a test video feed from the new hardware, and write a security sanitization filter for the incoming telemetry logs. 

Perform the following tasks:

1. **Backup and Tunneling Configuration**
We are replacing the old monitoring service. 
- Create a backup of the existing configuration directory located at `/home/user/legacy_monitor/` (create this directory and add a dummy file `config.json` to it first) to an archive at `/home/user/legacy_backup.tar.gz`.
- Write a bash script `/home/user/tunnel.sh` that sets up an SSH tunnel forwarding local port 9999 to `remote-telemetry.internal:80` via user `deploy@bastion.internal`. (You do not need to run this script, just write it accurately).

2. **Video Fixture Analysis (Health Check Simulation)**
The new camera firmware occasionally drops the feed, flashing a solid blue frame (where the central pixel at exactly center width/height is pure blue: Red=0, Green=0, Blue>250). 
We have captured a sample stream at `/app/deployment_test_feed.mp4`.
- Use `ffmpeg` and Python to process this video.
- Count the exact number of dropped (solid blue) frames.
- Write this integer count to `/home/user/dropped_frames.txt`.

3. **Adversarial Corpus: Telemetry Sanitizer**
The cameras send telemetry logs containing timestamp, locale, and timezone metadata. Recently, malicious actors have tried injecting shell commands into the `timezone` and `locale` fields of these JSON payloads.
- Write a Python script at `/home/user/sanitizer.py`.
- The script must accept a single file path as a command-line argument: `python3 /home/user/sanitizer.py <path_to_log.json>`
- The script must parse the JSON. If it detects any shell metacharacters (e.g., `;`, `|`, `&`, `$()`, backticks) or directory traversal attempts (`../`) in any string values, it must reject the file by exiting with status code `1` (Evil).
- If the file is benign, it must exit with status code `0` (Clean).
- Your script will be tested against a large corpus of clean and malicious logs. It must accurately distinguish between them without rejecting valid timezones (e.g., `America/New_York` or `en_US.UTF-8`).