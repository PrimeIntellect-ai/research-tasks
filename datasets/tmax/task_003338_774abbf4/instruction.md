You are a capacity planner analyzing resource usage from a legacy datacenter. The datacenter's old monitoring system outputs a visual feed of the server rack's status LED panel, which has been recorded and provided to you as a video file at `/app/monitoring_feed.mp4`. 

Your objective is to analyze this video to determine peak usage, build a custom reporting service in C to expose this data, and deploy it robustly.

**Phase 1: Video Analysis**
1. The video `/app/monitoring_feed.mp4` contains several hundred frames. The "high load" indicator is a square block of pixels in the top-left corner (from coordinates 0,0 to 15,15).
2. When the datacenter is under high load, this top-left 16x16 block turns bright red (Red > 200, Green < 50, Blue < 50). 
3. Use `ffmpeg` to extract the frames (e.g., to PPM format), and write a C program (e.g., `~/analyzer.c`) to parse the frames and count exactly how many frames show the "high load" indicator.
4. Record this total count.

**Phase 2: Configuration & Service Creation**
1. Create a configuration file at `~/server.conf` with the following format:
   ```
   PORT=8080
   HIGH_LOAD_FRAMES=<your_calculated_count>
   ```
2. Write a custom HTTP server in C (`~/server.c`) that reads `~/server.conf` on startup to get the port and the frame count.
3. The server must listen on the specified TCP port (8080) and handle HTTP/1.1 requests.
4. Implement two endpoints:
   - `GET /health`: Must return an `HTTP/1.1 200 OK` response with the body `OK`.
   - `GET /report`: Must return an `HTTP/1.1 200 OK` response with `Content-Type: application/json` and the body exactly matching: `{"high_load_frames": <COUNT>}`.

**Phase 3: Deployment & Monitoring**
1. Write a robust Bash supervisor script at `~/start.sh`.
2. The script must compile `~/server.c` to `~/server`, and then launch the server.
3. The script must monitor the server process. If the server exits or crashes, the script must automatically restart it.
4. Redirect all standard output and standard error from the server to `~/server.log`.
5. Start your supervisor script in the background (e.g., using `nohup ~/start.sh &` or similar) so the service is actively running and listening on port 8080 when you complete the task.

Do not use root privileges; run everything as the standard user. Ensure your C server correctly formats HTTP response headers (using `\r\n`).