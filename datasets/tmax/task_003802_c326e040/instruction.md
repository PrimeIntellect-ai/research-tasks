As a network security engineer, you have been provided with a screen recording of a suspected threat actor's terminal session. The video file is located at `/app/c2_terminal_screencast.mp4`. 

Your objective is to analyze the video, identify the exploit payload being constructed, and deploy a specialized Python honeypot service to intercept and log similar attacks.

**Step 1: Video Analysis (Reverse Engineering & Disassembly)**
The threat actor was recorded reverse engineering a proprietary authentication binary and constructing an SQL injection (SQLi) / Privilege Escalation payload. 
- Use `ffmpeg` (which is pre-installed) to extract the frames from `/app/c2_terminal_screencast.mp4`.
- Locate the frame displaying the final disassembled payload string (it will be visible in plain text within a debugger console in the video).
- Extract this exact SQLi payload string.

**Step 2: Honeypot Deployment (Protocol Analysis & Secure Coding)**
Write and execute a Python HTTP server that acts as a honeypot.
- The service must listen strictly on `127.0.0.1:9999`.
- It must expose a `POST` endpoint at `/login`.
- The endpoint should accept `application/json` data with a `username` field.
- If the `username` field exactly matches the malicious SQLi payload extracted from the video, the server must simulate a successful privilege escalation by returning an HTTP 200 response with the exact JSON body: `{"status": "escalated", "role": "root"}`.
- For all other inputs, return HTTP 403.

**Verification Requirements:**
Leave the Python honeypot running in the background. An automated verifier will issue an HTTP POST request to your service using the exact payload visible in the video to verify its correctness.