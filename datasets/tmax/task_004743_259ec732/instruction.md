You are a Site Reliability Engineer (SRE) investigating an ongoing issue with our legacy uptime monitoring pipeline. The pipeline consists of a Python service that calculates SLA metrics based on system logs and visual events from a legacy hardware dashboard. 

Recently, the SLA calculation service started crashing with a math-related traceback, and we suspect a regression was introduced in the local repository located at `/home/user/monitor_repo`. Additionally, there appears to be a subtle timezone bug causing events from different services to be misaligned, leading to numerical instability (calculating the square root of negative time deltas).

Your task consists of the following steps:
1. **Video Analysis**: We have a recording of the legacy hardware dashboard at `/app/dashboard_feed.mp4`. Analyze this video to find the exact frame number where the main status indicator (a pure red pixel block at coordinates x:100, y:100) first appears. Write this frame number to `/home/user/failure_frame.txt`.
2. **Log Correlation**: Reconstruct the timeline between `/var/log/service_a.log` and `/var/log/service_b.log` (which are in different timezones) to find the corresponding system event for the failure.
3. **Regression Isolation**: Use `git bisect` in `/home/user/monitor_repo` to identify the commit that introduced the timezone-related numerical bug. Write the full hash of the bad commit to `/home/user/bad_commit.txt`.
4. **Service Fix and Deployment**: Fix the Python service (`server.py`) so it correctly normalizes all timestamps to UTC before calculation, avoiding the numerical crash.
5. **Run the Service**: Start the fixed Python HTTP service. It must listen on `127.0.0.1:8080`. The service must expose an endpoint at `POST /api/v1/sla` that accepts a JSON payload like `{"event_time": "2023-10-27T15:30:00Z"}` and requires the header `Authorization: Bearer uptime-token-2024`. It should return a 200 OK with a JSON response `{"status": "ok", "sla": <calculated_float>}`. Leave this service running in the background.

Ensure all instructions are followed precisely and the server is running securely on the specified port.