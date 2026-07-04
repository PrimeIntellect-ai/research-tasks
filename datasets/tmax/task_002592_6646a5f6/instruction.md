You are an operations engineer triaging an incident in our video ingestion pipeline. A recent update caused the pipeline on x86 servers to crash when processing certain corrupted inputs due to a signed integer overflow bug in a legacy C-extension. 

We have isolated the network traffic during the crash to a packet capture at `/app/traffic.pcap` and the resulting corrupted video file at `/app/incident.mp4`. 

Your objectives are:
1. **Video Analysis**: The overflow bug manifests visually as the video feed dropping to a completely black frame. Extract the frames of `/app/incident.mp4` and identify the exact 0-indexed frame number where the video first turns completely black. Write this integer to `/home/user/corrupted_frame.txt`.
2. **Root Cause Filter**: By analyzing `/app/incident.mp4` and `/app/traffic.pcap`, identify the malformed metadata payload (simulating the integer overflow) that triggers this crash. 
3. **Detector Creation**: Write a Python script at `/home/user/sanitizer.py` that takes a single file path as a command-line argument. The script must analyze the given video file's metadata and:
   - Exit with status code `0` if the video is safe (clean).
   - Exit with status code `1` if the video contains the malicious/corrupted overflow payload.

You have access to two directories to test your script:
- `/app/corpus/clean/`: Contains 10 safe `.mp4` files.
- `/app/corpus/evil/`: Contains 10 corrupted `.mp4` files that trigger the bug.

Your `/home/user/sanitizer.py` must perfectly classify all files in these two directories. You may use `ffmpeg`, `ffprobe`, `tcpdump`, and standard Python libraries.