You are a backup administrator tasked with archiving sensitive data and investigating a recent security incident in the server room. You must complete two distinct operations: analyzing the security camera footage and creating a backup manifest filter in C++.

**Part 1: Video Incident Analysis**
There is a security camera recording of the server room located at `/app/incident.mp4`. The video is recorded at 1 frame per second (1 fps). You need to extract the frames and find the exact second the incident occurred. 
1. Use `ffmpeg` to extract the frames from `/app/incident.mp4` into a standard image format (like PNG).
2. Write a script or command to analyze these frames. You are looking for the exact frame where the pixel at coordinates X=100, Y=100 turns completely white (RGB: 255, 255, 255). 
3. Write the 0-indexed frame number (e.g., if it happens on the very first frame, write `0`) to `/home/user/incident_frame.txt`.

**Part 2: Backup Manifest Filter**
During the incident, the attacker attempted to corrupt our backup manifests to redirect archiving operations to unauthorized external IP addresses.
You must write a C++ program that serves as a classifier to detect these malicious modifications.

1. Create a C++ program named `/home/user/filter_manifest.cpp` and compile it to `/home/user/filter_manifest`.
2. The program must accept a single command-line argument: the absolute path to a manifest text file.
3. The program must read the file and parse it. Each manifest file contains a line in the format `TARGET_IP=<IP_ADDRESS>`.
4. **Clean vs. Evil Logic:** A manifest is considered **CLEAN** if and only if the `TARGET_IP` falls within our secure internal subnet: `10.0.0.x` (where x is between 0 and 255). If the IP address does not start with `10.0.0.`, or if the file is malformed, it is considered **EVIL**.
5. **Output Requirement:** If the file is CLEAN, the C++ program must terminate with an exit code of `0`. If the file is EVIL, it must terminate with an exit code of `1`.

We have provided a sample of backup manifests for you to test your C++ program:
- `/app/corpus/clean/` contains known good manifests.
- `/app/corpus/evil/` contains known malicious manifests.

Your compiled `/home/user/filter_manifest` binary will be automatically tested against a hidden set of clean and evil files to ensure 100% accuracy.