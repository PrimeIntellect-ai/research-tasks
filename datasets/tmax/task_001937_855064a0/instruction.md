As a backup operator, you need to test the integrity of our recovered legacy audio archives. An automated restore job has dropped a recovered audio file at `/app/voicemail_backup.wav`. 

You must build a "Restore Verification Service" written in Go and a process supervisor in Bash to ensure the service remains highly available.

Here are the requirements for the system:

1. **The Go Verification Service:**
   Create a Go application at `/home/user/restore_svc/main.go`. This service must run two concurrent servers:
   
   **HTTP API (Information Endpoint):**
   * Listen on `127.0.0.1:8080`.
   * Expose the endpoint `GET /api/v1/audio-meta`.
   * It must require an HTTP header exactly matching: `Authorization: Bearer operator-token-8831`.
   * When queried, the Go service must analyze the file `/app/voicemail_backup.wav` (using pure Go or by executing `ffprobe`/`ffmpeg` if available) and return a JSON response exactly matching this structure:
     `{"filepath": "/app/voicemail_backup.wav", "duration_seconds": <float64>, "size_bytes": <integer>}`
   * If the authorization header is missing or incorrect, return a 401 Unauthorized status code.

   **TCP Health Check (Monitoring Endpoint):**
   * Listen on `127.0.0.1:8081` (TCP).
   * Any client connecting and sending the exact string `STATUS\n` should receive the response `OK\n`, after which the server should close the connection.

2. **Process Supervision & Lifecycle:**
   * Since we don't have root access to configure systemd, write a bash script at `/home/user/watchdog.sh`.
   * The script must compile the Go application, start it, and continuously monitor the process.
   * If the Go process terminates or crashes, the watchdog must restart it within 2 seconds.
   * Standard output and standard error from the Go service must be appended to `/home/user/restore_service.log`.
   * Ensure `watchdog.sh` is executable.

To complete the task, leave the `watchdog.sh` script running in the background so the Go service is listening on both ports.