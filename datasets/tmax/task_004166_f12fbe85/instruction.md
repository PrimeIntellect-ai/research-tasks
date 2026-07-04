You are a deployment engineer tasked with rolling out a new monitoring service for a recent deployment, but the environment is currently misconfigured. You need to write a monitoring daemon in Go, configure it as a user-level service, and set up local port forwarding to expose its metrics securely.

**Part 1: Fix Local Port Forwarding**
There is a local SSH configuration in `/home/user/.ssh/config` that is intended to forward port 9090 to port 8080 on localhost. However, it is silently failing (key-based login is being rejected due to a misconfiguration resembling a silent reject policy, likely bad permissions or a strict `IdentitiesOnly` directive with a missing key). 
Fix the SSH configuration and permissions so that you can run `ssh -N -f local-monitor` to establish the tunnel without being prompted for a password.

**Part 2: Build the Monitoring Daemon in Go**
Create a Go program at `/home/user/monitor/main.go` that does the following:
1. **Storage Monitoring**: Calculates the total disk usage (in bytes) of all files inside `/home/user/deploy_artifacts/` (create this directory and add a few dummy files to test).
2. **Video Analysis**: An automated deployment dashboard recording is located at `/app/dashboard.mp4`. The daemon must use `ffmpeg` (or any Go wrapper) to extract frames at 1 frame per second. It must calculate the "error fraction": the number of extracted frames that contain a significant amount of pure red pixels (where R > 150, G < 50, B < 50 for at least 5% of the frame's pixels) divided by the total number of extracted frames.
3. **HTTP Server**: Expose an HTTP GET endpoint at `127.0.0.1:8080/metrics` that returns a JSON response in this exact format:
   ```json
   {
     "disk_usage_bytes": 1048576,
     "error_fraction": 0.34
   }
   ```

Compile the Go program to `/home/user/monitor/monitor_daemon`.

**Part 3: Service Configuration**
Write a valid systemd user service file at `/home/user/.config/systemd/user/monitor.service` that would manage this Go daemon. Since systemd might not be fully active in this container environment, also manually start your compiled daemon in the background so that it is actively listening on port 8080.

Ensure the SSH tunnel is active so that `curl http://127.0.0.1:9090/metrics` successfully returns the JSON payload. Leave the daemon and the SSH tunnel running.