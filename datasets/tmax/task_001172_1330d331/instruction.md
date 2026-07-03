Hello, I need help fixing and hardening our audio processing pipeline. The system processes audio alerts, but it's currently broken and needs some security improvements. 

Here is what you need to do:

1. **Service Fix**: There is a systemd service called `audio-processor.service` located in `/home/user/.config/systemd/user/`. It is currently failing to start because it tries to bind to a network interface before it's ready. Fix the service file so it starts successfully (it should wait for the network to be ready). Start and enable the service.

2. **Audio Transcription Check**: The service processes audio files. There is a sample audio file located at `/app/alert_sample.wav`. Use a command-line tool (like `ffmpeg` or a python script using standard libraries) to determine the exact duration of this audio file in seconds, rounded to two decimal places. Save this duration to `/home/user/audio_duration.txt`.

3. **Storage Monitoring**: Create a cron job for the current user that runs a bash script every 5 minutes. The script should be located at `/home/user/monitor_storage.sh`. It should check the disk usage of the `/home/user/audio_archive` directory. If the directory exceeds 50MB, it should append the current timestamp and the string "QUOTA_EXCEEDED" to `/home/user/storage_alerts.log`.

4. **Configuration Sanitizer**: We receive configuration files from various sources, and we need to filter out malicious ones. Write a Python script at `/home/user/sanitize_config.py`. The script should take a file path as an argument. It must read the file and determine if it's "safe" or "malicious". 
   - A file is malicious if it contains any string matching a shell execution pattern (e.g., `$(...)`, `` `...` ``) or tries to access `/etc/passwd` or `/etc/shadow`.
   - The script should exit with status code 0 if the file is safe, and status code 1 if it is malicious. 
   - The automated grader will test your script against a directory of clean files and a directory of evil files.

5. **Reverse Proxy Setup**: Set up a lightweight reverse proxy using Python's built-in `http.server` or a basic Python script. The proxy should run on port `8080` and forward all traffic to our backend service running on port `9090`. Save the script as `/home/user/proxy.py` and ensure it runs in the background.

Please ensure all scripts are executable and everything is placed exactly where specified.