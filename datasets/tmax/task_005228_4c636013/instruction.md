You are acting as a capacity planner for our data center. We need to analyze both physical access patterns and server resource utilization logs to plan our next infrastructure expansion.

There are three main parts to this task:

1. **Storage Setup**:
   Create a 100MB ext4 image file at `/home/user/capacity_data.img`.
   Mount it at `/home/user/mnt/capacity` using loopback. Make sure to add an entry in `/home/user/fstab_mock` (simulating `/etc/fstab`) that would mount this image with the `noexec` and `nodev` options.

2. **Physical Access Analysis (Video)**:
   We have a security camera video located at `/app/server_room_timelapse.mp4`.
   Using Python and `ffmpeg`, extract frames from this video at 1 frame per second. 
   Write a Python script `/home/user/analyze_video.py` that processes these frames (you can use simple motion detection or brightness thresholding, as the video flashes white when the door opens). The script should output a JSON file at `/home/user/mnt/capacity/access_counts.json` with a single key `"door_open_events"` mapped to the integer count of times the door opened.

3. **Resource Log Sanitization (Adversarial Corpus)**:
   We receive capacity resource logs from various servers, but some nodes are compromised and send malformed or malicious payload logs.
   Write a Python filter script at `/home/user/sanitize_logs.py` that reads a directory of log files and copies only the valid, safe logs to a destination directory, completely rejecting files containing malicious payloads.
   The script must be invoked as: `python3 /home/user/sanitize_logs.py --input <input_dir> --output <output_dir>`
   A valid log file contains lines with `TIMESTAMP HOSTNAME CPU_USAGE MEMORY_USAGE` (e.g., `2023-10-12T10:00:00Z server-1 45% 2.3GB`).
   A malicious log file contains SQL injection attempts, non-ASCII binary garbage, or shell metacharacters (`;&|`) in the hostname or usage fields. 

Execute your scripts and ensure the output JSON is generated and the log sanitizer is fully functional.