You are a container specialist managing a legacy microservice architecture. One of the old monitoring tools does not have an API and only outputs a recorded video of its dashboard `/app/dashboard_feed.mp4`. 

Your task involves setting up a data extraction pipeline and a supervised deployment monitor.

1. **Video Extraction**: Write a Python script to process `/app/dashboard_feed.mp4`. For every frame in the video, calculate the percentage of "red" pixels. Define a red pixel as having an RGB value where R > 150, G < 50, and B < 50. 
Output these values to a CSV file at `/home/user/extracted_metrics.csv` with exactly two columns: `frame` (integer index starting at 0) and `red_pct` (float from 0.0 to 100.0).

2. **Process Supervision**: Write a Python script `/home/user/monitor_service.py` that reads `/home/user/extracted_metrics.csv` and simulates monitoring by appending each value to a log file `/home/user/logs/monitor.log`. 
Set up `supervisord` in user-space (using a configuration file at `/home/user/supervisord.conf`) to run this Python script as a daemon. Ensure the process is set to auto-restart if it crashes.

3. **Log Rotation**: Create a logrotate configuration file at `/home/user/logrotate.conf` to manage `/home/user/logs/monitor.log`. Configure it to rotate the log file daily, keep 3 backups, compress old logs, and missing logs should be ignored.

4. **Timezone Configuration**: Ensure that the `monitor_service.py` writes its timestamps in the `Etc/UTC` timezone by explicitly handling it in the script or setting the `TZ` environment variable in the supervisord configuration.

Ensure all services are properly configured and files are placed exactly as requested.