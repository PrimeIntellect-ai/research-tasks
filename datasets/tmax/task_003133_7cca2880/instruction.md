You are an on-call engineer responding to a critical 3am page. Our automated physical security pipeline has triggered an alert, but the evidence extraction script is failing.

The system captured network traffic during an intrusion event and saved it to `/app/trigger.pcap`. At the exact same time the network capture started, a security camera started recording to `/app/camera.mp4`. 

The attacker sent a specific "trigger" packet: a TCP SYN packet destined for port 1337. We need to extract the exact video frame showing the camera's view at the moment that trigger packet was received.

The current extraction script, located at `/home/user/extract_evidence.sh`, is supposed to:
1. Parse `/app/trigger.pcap` to find the precise relative time (in seconds, from the start of the capture) of the first TCP SYN packet sent to destination port 1337.
2. Extract the single video frame from `/app/camera.mp4` at that exact relative time.
3. Save the resulting frame as `/home/user/evidence.jpg`.

Unfortunately, the original author wrote a script that extracts every single frame of the video to disk and attempts to calculate byte offsets manually, which causes out-of-memory errors and takes over 10 minutes before being killed by our watchdog.

Your task is to debug, fix, and optimize `/home/user/extract_evidence.sh` using efficient Bash commands and standard tools (like `tcpdump` or `tshark`, and `ffmpeg`). 

Requirements:
- The script must complete its execution in **under 3.0 seconds**.
- The extracted image `/home/user/evidence.jpg` must precisely match the frame at the time of the network trigger.
- The script must be completely self-contained and require no user interaction.
- The output file must be a standard JPEG image.

Do whatever it takes to rewrite the script so it efficiently and accurately fulfills these requirements.