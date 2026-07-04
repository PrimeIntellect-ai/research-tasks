You are an edge computing engineer deploying a secure telemetry gateway for our new batch of IoT devices. We have an isolated edge node where you must set up the gateway services, reverse proxy, and logging system without root privileges.

Due to a misconfiguration in our provisioning system, the device's authentication PIN was delivered as an audio message rather than text. 

Please perform the following tasks:

1. **Extract the Telemetry PIN**:
   - There is an audio file located at `/app/telemetry_pin.wav`.
   - Transcribe this audio file to retrieve a 4-digit numeric PIN. You may install and use any transcription tools you need (e.g., whisper.cpp, ffmpeg).

2. **Develop the C Telemetry Daemon**:
   - Write a C program in `/home/user/telemetry_daemon.c` and compile it to `/home/user/telemetry_daemon`.
   - The daemon must start and listen for incoming TCP connections on `127.0.0.1:9090`.
   - Upon receiving a connection, it should read exactly one line of text (ending in `\n`).
   - If the received text matches the format `AUTH <PIN>` (where `<PIN>` is the 4-digit numeric PIN from the audio file), the daemon must reply with `TELEMETRY_ACK\n`.
   - If the text does not match, it must silently close the connection (similar to an SSH config rejecting key-based logins without prompting).
   - Every connection attempt must be logged to `/home/user/logs/telemetry.log` with the format: `[TIMESTAMP] Connection received` (you can use standard Unix timestamps).

3. **Configure the Reverse Proxy**:
   - Set up `haproxy` (running as the `user` account, no root required).
   - Create a configuration file at `/home/user/haproxy.cfg`.
   - The proxy should listen for TCP traffic on `0.0.0.0:8080`.
   - It should route incoming traffic to your C telemetry daemon at `127.0.0.1:9090`.
   - Start the HAProxy instance in the background. Ensure your C daemon is also running in the background.

4. **Implement Backup & Log Rotation Strategy**:
   - Write a shell script at `/home/user/rotate_and_backup.sh`.
   - When executed, the script must:
     - Move `/home/user/logs/telemetry.log` to `/home/user/backups/telemetry_$(date +%s).log`.
     - Send a signal or restart the C daemon so it creates a fresh `telemetry.log` file and continues operating.
     - Ensure the `/home/user/backups` directory exists.
   - Make the script executable.

Ensure the C daemon and HAProxy are running and actively listening on their respective ports by the time you complete your task.