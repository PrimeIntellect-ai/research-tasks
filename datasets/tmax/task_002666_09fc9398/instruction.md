I need you to write a Python script that acts as a secure filter for project archives submitted by external contractors. 

The contractors upload project files as `.zip` archives. Unfortunately, some of these archives are malicious and contain "Zip Slip" payloads (file paths that attempt to write outside the extraction directory using absolute paths or directory traversal sequences like `../`). 

Additionally, as part of our synchronization protocol, we record a video of the test run, which is available at `/app/test_run.mp4`. The video contains a sequence of black frames and exactly one pure blue frame (RGB: `0, 0, 255`).

Your task is to write a script at `/home/user/verify_archive.py` that validates an archive without safely extracting it to disk. 

The script must accept exactly one argument (the path to the `.zip` file) and exit with code `0` if the archive is completely valid, or exit with code `1` if it is invalid.

An archive is **valid** if and only if it meets ALL of the following criteria:
1. **Security (Zip Slip prevention):** The archive must NOT contain any file paths that would resolve outside the target extraction root directory. Reject any archive with absolute paths or relative traversal paths (`../`) that escape the root.
2. **Structure:** It must contain a text file named exactly `build.log` located at the root of the archive.
3. **Synchronization Metadata:** You must parse `build.log` (which contains multi-line log records). It must contain exactly the following multi-line block somewhere in the file:
   ```
   [EVENT]
   Status: SUCCESS
   Sync-Frame: <N>
   ```
   where `<N>` is the exact 0-indexed frame number of the single pure blue frame in the `/app/test_run.mp4` video.

Constraints:
- You must write the solution in Python (`/home/user/verify_archive.py`).
- You must read and inspect the archive structure and `build.log` contents entirely in memory (do not extract the archive to disk, as this is a security risk).
- Pre-installed tools like `ffmpeg` or `opencv-python` are available if you need them to process the video. 

Once you have created the script, let me know.