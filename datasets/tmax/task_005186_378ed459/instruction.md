You are a compliance analyst generating a secure audit trail for a recent security incident. An incident response recording has been captured as a video file at `/app/audit_video.mp4`. 

Your objective is to extract the video frames, compute a cryptographic hash chain of the frames using a highly optimized C++ implementation, and execute this process inside a strict, unprivileged sandbox to satisfy compliance policies.

Step 1: Frame Extraction
Use `ffmpeg` to extract the frames of `/app/audit_video.mp4` at 1 frame per second into a directory `/home/user/frames/`, naming them sequentially (e.g., `frame_0001.jpg`, `frame_0002.jpg`, etc.).

Step 2: Optimized C++ Hash Chain
A naive Python script at `/home/user/baseline.py` computes a cumulative SHA-256 hash chain of all files in a directory, but it is too slow for our large-scale compliance workloads. 
Write a highly optimized C++ program at `/home/user/hasher.cpp` and compile it to `/home/user/hasher`. The program must:
1. Accept a directory path as its first argument and an output file path as its second argument.
2. Read all `.jpg` files in the given directory in alphabetical order.
3. Compute a cumulative SHA-256 hash. Let H_0 = SHA256("init"). For each frame, H_i = SHA256(H_{i-1} + <raw binary contents of frame_i>).
4. Write the final hex-encoded SHA-256 hash to the output file.
5. Your C++ program will be graded on execution speed. It must process the frames significantly faster than the baseline script.

Step 3: Process Isolation Sandbox
To ensure the integrity of the hashing process, the binary must run in a restricted environment without network access.
Create a bash script at `/home/user/generate_trail.sh` that uses `bwrap` (Bubblewrap) to execute your `/home/user/hasher` program with the following constraints:
- Completely isolated network namespace (`--unshare-net`).
- Read-only access to `/home/user/frames/` and necessary system libraries (e.g., `/usr`, `/lib`, `/lib64`).
- Write access ONLY to `/home/user/audit_trail.txt`.
- No access to any other user directories or sensitive system files (e.g., hide `/etc`, `/tmp`).

Run your script so that `/home/user/audit_trail.txt` is generated successfully containing the final hash.