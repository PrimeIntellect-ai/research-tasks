You are a FinOps Analyst working to optimize our cloud resource usage and prevent runaway costs in our infrastructure. We have two primary tasks for you to complete involving incident forensics and CI/CD cost prevention.

**Task 1: Incident Forensics (Video Analysis)**
We experienced a severe billing spike yesterday due to a rogue crypto-miner process that temporarily hijacked our servers. We have a screen recording of our infrastructure monitoring dashboard located at `/app/dashboard_recording.mp4`. 
The monitoring software displays a pure red square (RGB: 255, 0, 0, at least 50x50 pixels) on screen whenever CPU usage exceeds 99%.
You must extract the frames from this video and analyze them to determine the exact duration of the attack. 
Find all frame numbers where this pure red square is visible. Write these frame numbers as a comma-separated list into the file `/home/user/spike_frames.txt`. (e.g., `12,13,14,15`).

**Task 2: Preventive Cost Filter (Git Hook Simulation)**
To prevent developers from accidentally pushing massive assets or bloated log files that consume expensive CI/CD EBS storage quotas, we need a repository filter.
Write a Python script at `/home/user/cost_filter.py` that acts as a simulated Git pre-receive hook.
The script must take exactly one command-line argument: the path to a directory representing a proposed commit payload.
The script must recursively scan the provided directory and enforce our FinOps storage policies.

It must **reject** the directory if ANY of the following conditions are met:
1. Any file in the directory tree is strictly larger than 100,000 bytes.
2. Any file in the directory tree has the extension `.dump`, `.iso`, or `.mp4`.
3. Any file contains the exact string `[COST_ALERT: MASSIVE_LOG]` anywhere in its contents.

If the directory violates any of these policies, your script must print `REJECT` to standard output and exit with status code `1`.
If the directory passes all checks, your script must print `ACCEPT` to standard output and exit with status code `0`.

Ensure your script is robust and handles nested directories and standard file reading properly. You are free to use `ffmpeg`, `opencv-python`, `Pillow`, or any standard tools for the video analysis part.