You are an edge computing engineer deploying a new data ingestion and physical security gateway for remote IoT devices. You need to automate the deployment, create a payload sanitizer to drop malicious incoming requests, and analyze a diagnostic video feed to detect physical tampering.

Complete the following objectives using bash and Go:

1. **Payload Sanitizer (Go)**
Write a Go program at `/home/user/sanitizer.go` and compile it to `/home/user/sanitizer_bin`.
This binary will be used as a pre-filter for an edge API. It must read a JSON payload from `stdin` and validate it.
A valid payload must have exactly these fields (and no others are relevant for validation, though extra fields are allowed if the required ones are perfect):
- `device_id`: string, exactly 8 alphanumeric characters.
- `ip_address`: string, a valid IPv4 address.
- `temperature`: float, must be between -50.0 and 150.0 (inclusive).

If the payload is perfectly valid, the program must exit with status code `0`.
If the payload is malformed, invalid, or contains out-of-bounds/malicious data for the specified fields, the program must exit with status code `1`.
*Note: A test suite will evaluate your binary against two hidden corpora: `/app/corpus/clean/` (which must all exit 0) and `/app/corpus/evil/` (which must all exit 1).*

2. **Physical Tamper Detection (Video Analysis)**
The edge device has a light sensor camera inside its dark enclosure. If the enclosure is opened, light leaks in. A recent 10-second diagnostic recording is available at `/app/camera_feed.mp4` (10 FPS, 100 frames).
Use `ffmpeg` and basic shell utilities (or a short Go script) to analyze the frames. Find the exact frame numbers (0-indexed, from 0 to 99) where the average grayscale brightness of the frame indicates the box was opened (e.g., significant non-black pixels).
Write the comma-separated list of these frame numbers to `/home/user/tamper_frames.txt` (e.g., `12,13,14`).

3. **Network Configuration & Automation**
Write a bash script at `/home/user/deploy.sh` (ensure it is executable) that does the following:
- Exports an environment variable `EDGE_NODE=active_secure`.
- Writes the exact SSH command required to create a background SSH tunnel that forwards local port `8080` to remote port `9090` on `localhost` (running in the background without executing remote commands) into a file named `/home/user/tunnel_cmd.txt`.
- Compiles your `/home/user/sanitizer.go` to `/home/user/sanitizer_bin`.

Ensure all requested files (`sanitizer.go`, `sanitizer_bin`, `tamper_frames.txt`, `deploy.sh`, `tunnel_cmd.txt`) are present in `/home/user/` when you finish.