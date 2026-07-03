You are a network engineer tasked with troubleshooting and maintaining a proprietary, highly unstable network telemetry daemon. 

We have a legacy, stripped binary located at `/app/net_worker` that performs continuous connectivity checks. Unfortunately, it is extremely poorly written:
1. It is prone to random crashes (it exits unpredictably).
2. It constantly writes bulky diagnostic cache data to `/home/user/cache/data.bin`. If this file grows larger than 8MB, the daemon will completely hang and stop processing network checks, though the process remains alive.

Your task is to write a robust bash supervisor script at `/home/user/supervisor.sh` that performs the following multi-stage workflow:

1. **Environment & System Config:** Ensure the directory `/home/user/cache/` and `/home/user/backups/` exist. Create a basic configuration file at `/home/user/config.ini` with the content `mode=active`. Before starting the daemon, your script must create a backup of this config file at `/home/user/backups/config.ini.bak`.
2. **Execution & Health Monitoring:** Run `/app/net_worker` in the background. You must constantly monitor its process state. If it dies or crashes, your script must automatically restart it.
3. **Storage Quota & Backup Strategy:** You must monitor the size of `/home/user/cache/data.bin`. If the file exceeds 5MB (5242880 bytes), you must immediately move it into `/home/user/backups/`, append a timestamp to the filename (e.g., `data_1610000000.bin`), gzip it, and let the daemon create a fresh `data.bin`. This ensures the daemon never hits the 8MB stall limit.
4. **Integration:** Your `supervisor.sh` must run continuously (using an infinite loop with a short `sleep` interval for checks) to handle restarts and log rotation seamlessly.

The daemon writes a `[PACKET_OK]` line to `/home/user/net.log` every time it successfully completes a network check (about 10 times a second). 

We will verify your solution by running your `supervisor.sh` script for exactly 20 seconds and then terminating it. We will then count the number of `[PACKET_OK]` lines in `/home/user/net.log`. To succeed, your supervisor must ensure high uptime and prevent the daemon from stalling, maximizing the number of processed packets.

Make sure your script is executable (`chmod +x /home/user/supervisor.sh`).