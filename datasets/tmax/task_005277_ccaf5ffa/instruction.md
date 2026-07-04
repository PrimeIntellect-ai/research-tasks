We recently experienced a widespread monitoring incident where our automated deployments failed. An unknown configuration drift caused SSH key-based logins to fail silently on several servers, triggering a cascade of alerts. We need you, our monitoring specialist, to build an automated diagnostic pipeline to triage this issue.

**Part 1: Video Alert Analysis**
Our legacy alerting dashboard doesn't output text logs; instead, it flashes a red indicator on a screen recording when an SSH timeout occurs. We have captured a video of the dashboard during the incident, located at `/app/monitor_feed.mp4`.
1. Use `ffmpeg` and Python to analyze the video.
2. Identify all frames where the pixel at exactly `x=10, y=10` (top-left area) is pure red (RGB: 255, 0, 0).
3. The video recording started exactly at `2024-03-15 14:00:00 UTC`.
4. For every frame where the alert indicator is pure red, calculate its exact time. Convert that time to the `Asia/Tokyo` timezone (JST).
5. Output these timestamps to `/home/user/alert_timestamps.txt`, one per line, strictly in the format: `YYYY-MM-DD HH:MM:SS JST`. Round the seconds down to the nearest integer.

**Part 2: SSH Config Linter (Adversarial Detection)**
The root cause was a subtle manipulation of the `sshd_config` file that silently rejects key-based logins while appearing normal to standard linters (e.g., overriding `AuthorizedKeysFile` to `/dev/null`, setting `PubkeyAcceptedKeyTypes none`, or forcing `AuthenticationMethods password` while leaving `PubkeyAuthentication yes` intact).

We have extracted a corpus of known good configs at `/app/corpus/clean/` and known compromised configs at `/app/corpus/evil/`.
1. Write a Python script at `/home/user/check_ssh_config.py` that takes a single command-line argument: the path to an `sshd_config` file.
2. The script must analyze the config file and determine if it contains any of these silent key-rejection traps.
3. If the file is compromised (evil), the script must print exactly `EVIL` to stdout and exit with code `1`.
4. If the file is safe (clean), the script must print exactly `CLEAN` to stdout and exit with code `0`.
5. We will test your script against a hidden holdout set of configs. It must achieve 100% accuracy.

Ensure your Python script is robust, executable, and handles standard SSH config parsing rules (e.g., ignoring comments and handling whitespace).