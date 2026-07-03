You are a network engineer investigating a sudden connectivity drop in a remote datacenter. The automated PBX monitoring system left an emergency voicemail alert containing the IP address of the failing network node. 

Your task involves transcribing this alert to identify the failing node, and then building a custom C++ diagnostic daemon to report the fault and manage incoming network logs.

Step 1: Extract the IP Address
You will find the automated audio alert at `/app/incident_alert.wav`. Listen to or transcribe this audio file to extract the IPv4 address of the failing node. Tools like `whisper-cli`, `ffmpeg`, or Python libraries are available in your environment.

Step 2: Build the Diagnostic Daemon
Write a C++ program at `/home/user/diag_daemon.cpp` and compile it to `/home/user/diag_daemon`. This daemon must perform two primary functions simultaneously:

Function A: Telemetry Server
The daemon must run an HTTP server listening on `127.0.0.1:8080`. 
When it receives an HTTP `GET /api/v1/fault` request, it must respond with an HTTP 200 OK and a JSON payload formatted exactly like this:
`{"faulty_ip": "<IP_EXTRACTED_FROM_AUDIO>", "log_status": "active"}`
Make sure to include appropriate HTTP headers (Content-Type: application/json, Content-Length).

Function B: Log Rotation and Permission Management
Our diagnostic tools constantly write to a log file at `/home/user/net_logs/traffic.log`. 
Your daemon must monitor this file. Whenever `traffic.log` exceeds 500 bytes in size, your daemon must:
1. Rotate the log by moving it to `/home/user/net_logs/archive/traffic_<UNIX_TIMESTAMP>.log` (where `<UNIX_TIMESTAMP>` is the current integer epoch time).
2. Immediately set the filesystem permissions of the archived log file to strictly read-only (`0444`), preventing any further modifications.
3. Allow the external tools to safely create a new `traffic.log` (if you moved the file, the external tools will automatically recreate it).

Setup instructions:
- Ensure you create the directories `/home/user/net_logs/archive/` before starting your daemon.
- Leave your compiled daemon running in the background listening on port 8080 so the automated verification system can interact with it.
- Do not use any third-party C++ frameworks (like Boost or Crow) for the HTTP server; use standard POSIX sockets (`<sys/socket.h>`) and standard C++ libraries (`<fstream>`, `<sys/stat.h>`, etc.).