You are an observability engineer tasked with tuning our filesystem dashboards. We have a historical video recording of our physical disk monitoring dashboard located at `/app/dashboard_capture.mp4`. Due to a legacy system quirk, critical filesystem alerts (inode exhaustion) were logged as solid red flashes in this dashboard video stream rather than text logs.

Your task is to build a Go-based observability exporter that analyzes this video, recovers the alert count, and serves the metrics over a protected HTTP endpoint. 

Follow these requirements to set up the system:

1. **Video Analysis (Go)**
   - Write a Go application at `/home/user/obs/exporter.go` that reads `/app/dashboard_capture.mp4`.
   - The application should extract frames (e.g., using `ffmpeg` as a subprocess or a library) and count the number of "CRITICAL INODE" frames.
   - A frame is defined as a "CRITICAL INODE" frame if its average RGB values across all pixels satisfy: Red > 200, Green < 50, Blue < 50.

2. **Metrics Server (Go)**
   - The Go application must run a persistent HTTP server.
   - Read the port from the `OBS_PORT` environment variable (it will be set to `9090`).
   - Implement a health check endpoint at `/health` that returns `200 OK`.
   - Implement a metrics endpoint at `/metrics`. This endpoint MUST require an `Authorization: Bearer <token>` header, reading the token from the `OBS_TOKEN` environment variable.
   - The `/metrics` endpoint should return the Prometheus-formatted metric: `critical_inode_frames_total <count>`.

3. **Process Supervision & Environment**
   - Create a shell script `/home/user/obs/start.sh` that sets `OBS_PORT=9090` and `OBS_TOKEN=OBS-TUNING-2024`, builds the Go binary, and runs it in an infinite `while true` loop (to automatically restart it if it crashes).
   - The script must redirect all standard output and standard error of the Go application to `/home/user/obs/metrics.log`.
   - Start this wrapper script in the background.

4. **Log Rotation**
   - Create a logrotate configuration file at `/home/user/obs/logrotate.conf` to rotate `/home/user/obs/metrics.log`.
   - The rotation policy should be: daily, keep 3 backups, compress old logs, and copytruncate.
   - Add a scheduled task (cron) for the `user` to run `logrotate /home/user/obs/logrotate.conf` every hour.

Once you are done, leave the background supervision script running so the HTTP service remains active.