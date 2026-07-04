You are a Linux systems engineer tasked with building and hardening a custom video analysis network daemon. We need a reliable, supervised network service written in C that reports metadata about a piece of surveillance footage while running under strict environment controls.

Your task consists of the following steps:

1. **Video Analysis**:
   There is a video file located at `/app/surveillance.mp4`. You need to determine the exact total number of frames in this video. 

2. **C Network Daemon (`/home/user/server.c`)**:
   Write a raw TCP server in C that binds to `127.0.0.1:8888`. It must accept incoming TCP connections and respond to the following newline-terminated (`\n`) text commands:
   - `COUNT\n` : The server must respond with the total frame count of the `/app/surveillance.mp4` video (e.g., `142\n`). It is recommended to calculate this once at startup or hardcode your finding to avoid invoking heavy shell commands per request.
   - `TIME\n` : The server must respond with the current local time formatted exactly as `YYYY-MM-DD HH:MM:SS %Z` (e.g., `2023-10-25 14:30:00 JST\n`). The timezone must strictly be Japanese Standard Time (JST).
   - `CRASH\n` : The server must immediately simulate a fatal error by calling `exit(1)`.

   After responding to a command, the server should close the client socket (one command per connection).

3. **Hardened Compilation**:
   Compile your C program into the executable `/home/user/server`. You must apply the following security hardening flags exactly:
   `gcc -O2 -Wall -fPIE -pie -fstack-protector-strong -D_FORTIFY_SOURCE=2 -Wl,-z,relro,-z,now /home/user/server.c -o /home/user/server`

4. **Process Supervision (`/home/user/supervisor.sh`)**:
   Since the daemon is prone to crashing (simulated by the `CRASH` command), write a robust Bash supervisor script at `/home/user/supervisor.sh`. 
   - The script must configure the environment so the daemon strictly operates in the `Asia/Tokyo` timezone.
   - It must launch the `/home/user/server` daemon.
   - If the daemon exits for any reason, the supervisor must restart it within 1 second.
   - Run this supervisor script in the background before completing the task so the service is available.

Ensure your service is up and running on `127.0.0.1:8888` as the final state. An automated test will connect to this port and issue commands to verify functionality, timezone configurations, and restart policies.