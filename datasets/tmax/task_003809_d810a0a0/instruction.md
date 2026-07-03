You are a penetration tester analyzing artifacts from a breached sandbox environment. You have two objectives:

**Objective 1: Video Forensics**
A recording of the compromised sandbox's virtual terminal has been provided at `/app/sandbox_review.mp4`. During this execution, a sensitive isolation key was leaked to the screen.
1. Use `ffmpeg` to extract the frames of this video.
2. Use optical character recognition (`tesseract` is installed) to find the exact frame number where the text `EXPLOIT_SUCCESS` first becomes fully visible on the screen.
3. Write ONLY the integer frame number to `/home/user/exploit_frame.txt`.

**Objective 2: Leak Detector**
We need to prevent future sandbox logs from leaking sensitive data or executable payloads. Write a Python script at `/home/user/detector.py` that takes a single file path as a command-line argument.
The script must act as a classifier for sandbox process logs:
* Identify the file as **EVIL** (exit with status code `1`) if the file contains either:
  a) An unredacted sandbox secret, matching the exact format `SBX_SECRET_` followed by exactly 16 lowercase hexadecimal characters (e.g., `SBX_SECRET_a1b2c3d4e5f60718`).
  b) A hex-encoded ELF header. Look for the byte sequence `7f 45 4c 46` or `7f454c46` (ignoring spaces, case-insensitive) which indicates a binary payload has been dumped to the logs.
* Identify the file as **CLEAN** (exit with status code `0`) if it contains neither of these. Clean files might contain standard application logs, sanitized outputs, or non-ELF hex dumps.

Your `detector.py` will be tested against a hidden corpus of clean and evil files. It must successfully flag all malicious logs without raising false positives on benign logs.