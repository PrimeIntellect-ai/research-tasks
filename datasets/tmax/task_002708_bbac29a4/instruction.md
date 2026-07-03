You are tasked with setting up a custom log monitoring and filtering system for our servers.

First, analyze the video provided at `/app/server_status.mp4`. This video is a recording of an external diagnostic LED. You need to count the exact number of frames in the video that are completely, solidly red (where all pixels are strictly Red, i.e., RGB 255, 0, 0). Let this exact count be `N`.

Second, write an executable script at `/home/user/log_filter` in a language of your choice. This script will act as a health check filter. 
- It must read a single string from Standard Input (stdin).
- It must count the number of times the exact substring `ERROR` appears in the input string.
- If the count is strictly greater than `N` (the red frame count from the video), the script must output exactly `ALERT` followed by a newline to Standard Output (stdout).
- Otherwise, it must output exactly `OK` followed by a newline.

Third, ensure standard administrative practices:
- Create a dummy log file at `/var/log/health.log` with appropriate permissions.
- Create a logrotate configuration at `/etc/logrotate.d/health_monitor` that rotates `/var/log/health.log` daily, keeps 7 backups, and compresses them.

Your script `/home/user/log_filter` will be subjected to extensive random fuzz-testing against a secret reference implementation to ensure strictly identical behavior.