You are a network engineer troubleshooting a connectivity issue during a rolling deployment of our internal services. We captured a screen recording of the deployment dashboard during the incident, but the dashboard server crashed and the only record we have is the video file.

Your objective is to identify the healthy service ports from the video, configure our legacy router using an Expect script, and stand up a Bash-based API gateway to route traffic.

Step 1: Video Analysis
A recording of the incident is located at `/app/network_glitch.mp4`. Use `ffmpeg` to extract the frames and inspect them (you can use `tesseract` for OCR or simply look at the extracted images). The video displays the status of several backend nodes. Identify the three port numbers that are explicitly marked as "STABLE".

Step 2: Expect Scripting for Legacy Router
Our legacy router configuration tool is an interactive script located at `/app/legacy_router_cli`. It cannot accept command-line arguments. 
Write an Expect script at `/home/user/configure.exp` that automates interaction with this tool.
The tool prompts for:
1. "Username: " -> You must provide `admin`
2. "Password: " -> You must provide `netops`
3. "Enter STABLE ports space-separated: " -> You must provide the three STABLE ports you found in the video, in ascending numerical order, separated by spaces.
Once successful, the tool will generate a configuration file at `/home/user/router.cfg`.

Step 3: Bash API Gateway Daemon
Write a Bash script at `/home/user/gateway.sh` that acts as a simple API gateway and health-check responder. The script must do the following:
1. Run indefinitely in the background (implement proper lifecycle management: write its PID to `/home/user/gateway.pid` so it can be cleanly stopped).
2. Read the STABLE ports from `/home/user/router.cfg`.
3. Listen for HTTP GET requests on `127.0.0.1:8888`. When a request is made to `/status`, it must respond with a valid HTTP/1.1 200 OK response, and the body must exactly match the contents of `/home/user/router.cfg`.
4. Listen for raw TCP connections on `127.0.0.1:8889`. When any data is received, it must immediately reply with the string `SYNC_ACK\n` and close the connection.

Ensure your gateway script is running and functional before finishing the task. We will verify your deployment by sending real HTTP and TCP requests to your gateway.