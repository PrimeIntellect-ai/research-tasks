You are a system administrator investigating a potential security incident involving unauthorized access and rogue processes. 

Part 1: Video Analysis
We have a screen recording of an internal monitoring dashboard at `/app/dashboard_monitor.mp4`. During the recording, an alert indicator flashes pure red (RGB: 255, 0, 0) for exactly one frame to indicate a breach time. 
Use `ffmpeg` and Python to extract and analyze the frames. Find the exact frame number (0-indexed) where a pure red pixel appears anywhere in the frame. Write this integer frame number to `/home/user/breach_frame.txt`.

Part 2: Malicious SSH Tunnel Detector
The attacker established rogue SSH tunnels to bypass our firewall. You need to write a robust Python script at `/home/user/detect_tunnels.py` to identify malicious SSH port forwarding from process logs.

The script must:
1. Accept a single command-line argument: the path to a text file containing the output of `ps -eo args`.
2. Parse the file to find any `ssh` commands.
3. Determine if any `ssh` process is performing port forwarding (specifically looking for `-L`, `-R`, or `-D` flags, considering variations in spacing and combined flags like `-NL`).
4. Exit with code `0` if the file is completely CLEAN (only normal SSH connections, e.g., `ssh user@host`, `ssh -p 22 -i key.pem user@host`).
5. Exit with code `1` if the file is EVIL (contains at least one rogue SSH tunnel command).

Ensure your script is robust against missing files, malformed lines, and standard error handling. 
Your script will be tested against a hidden corpus of clean and evil logs.