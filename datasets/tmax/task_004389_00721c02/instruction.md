You are a Site Reliability Engineer tasked with auditing the historical uptime of a legacy system that only reports its status via a physical LED light. We have a 10-second video recording of this status light located at `/app/status_light.mp4`. 

Your goal is to analyze this video, calculate the system's uptime, archive the downtime evidence, configure an automated alert, and expose the uptime metrics via a multi-protocol service.

Please perform the following steps:

1. **Video Analysis**:
   - The video `/app/status_light.mp4` shows a solid color representing the server's status: Green (server is UP) or Red (server is DOWN).
   - Extract the frames and count the number of Green frames and Red frames.
   - Calculate the uptime percentage: `(Green frames / Total frames) * 100`. Round this to exactly 2 decimal places (e.g., `83.33`).

2. **Downtime Backup Strategy**:
   - Extract all the Red frames (where the server was down) as PNG files.
   - Create a compressed tarball at `/home/user/downtime_backup.tar.gz` containing only these red frames.
   - *Note: You must only include the red frames in this archive.*

3. **Expect Scripting for Alerting**:
   - There is an interactive script at `/app/trigger_alert.sh` that notifies the on-call team.
   - Write an `expect` script at `/home/user/alert.exp` that automates interaction with this script.
   - Your expect script must spawn `/app/trigger_alert.sh`.
   - When prompted with exactly `Enter server uptime percentage:`, it must send the calculated uptime percentage.
   - When prompted with exactly `Confirm alert dispatch (y/n):`, it must send `y`.
   - Ensure the expect script runs to completion.

4. **Multi-Protocol Metric Service**:
   - Write and run a multi-language or Python service that listens continuously in the background on the following ports:
     - **HTTP on port 8080**: Any `GET` request to the endpoint `/api/status` must return a JSON payload with the exact format: `{"uptime_percent": <calculated_value>}` (e.g., `{"uptime_percent": 83.33}`). It must return an HTTP 200 OK status.
     - **Raw TCP on port 8081**: Any TCP client that connects to this port should immediately receive the string `UPTIME:<calculated_value>\n` (e.g., `UPTIME:83.33\n`) and then the connection must be closed by the server.

You can use any installed tools (ffmpeg, python3, bash, expect) to complete this task. Leave the multi-protocol service running in the background when you are finished.