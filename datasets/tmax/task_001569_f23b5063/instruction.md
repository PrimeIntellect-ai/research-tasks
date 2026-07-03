You are a storage administrator managing a massive data cluster. Recently, a malicious user exploited an automated log extraction script by uploading an archive containing path traversal filenames (a "zip-slip" attack), which overwrote critical system configuration files.

You must build a Secure Storage Monitor to analyze the attack footprint and prevent future occurrences. 

Your objective is split into three phases:

**Phase 1: Video Forensics**
During the attack, a legacy monitoring tool was recording the console output. The screen recording has been saved to `/app/console_recording.mp4`.
1. Use `ffmpeg` and `tesseract-ocr` (you may install it via `sudo apt-get update && sudo apt-get install -y tesseract-ocr`) to extract frames and analyze the text.
2. Count exactly how many individual frames contain the exact string `BREACH_DETECTED`. Keep this count for the daemon in Phase 3.

**Phase 2: Metadata Search**
The attacker left traces in our metadata storage. 
1. Search the directory `/app/storage_metadata/` recursively for JSON files.
2. Find all JSON files that are strictly greater than 10KB in size AND contain the exact key-value pair `"status": "compromised"` (accounting for standard JSON formatting/spacing).
3. Write the absolute paths of these files to `/home/user/compromised_files.txt`, one path per line.

**Phase 3: Secure Daemon Implementation (C)**
Write a C daemon at `/home/user/daemon.c` and compile it to `/home/user/daemon`. The daemon must listen on TCP port `5050` at `127.0.0.1` and implement a custom text-based protocol. It must handle one connection at a time (sequential is fine) and keep the connection open until closed by the client.

Protocol specifications:
- The daemon must read newline-terminated (`\n`) commands.
- `AUTH <token>\n`: The client must authenticate first by sending `AUTH storage_sec_token_v1\n`. If a client sends any other command before authenticating, or provides the wrong token, immediately close the connection. Reply with `OK\n` upon success.
- `VIDEO_COUNT\n`: Reply with the exact frame count found in Phase 1 in the format `COUNT: <N>\n`.
- `INSPECT <absolute_path_to_tar>\n`: The daemon must open the uncompressed POSIX ustar tar archive at the given path. **Do not use external commands like `tar` or `system()`.** You must parse the 512-byte tar headers directly in C using File I/O. Check the file name field (offset 0, 100 bytes). If *any* file name in the archive starts with `/` or contains `../`, immediately reply `MALICIOUS\n`. If the end of the archive is reached and all files are safe, reply `SAFE\n`.
- `WATCH <absolute_directory_path>\n`: The daemon must use Linux `inotify` to begin watching the specified directory. Reply with `WATCHING\n`. Whenever a new file is fully written and closed in that directory (`IN_CLOSE_WRITE`), the daemon must:
  1. Inspect the file as a tarball (using the same logic as `INSPECT`).
  2. Append a log entry to `/home/user/archive_watch.log` in the format: `[NEW_FILE] <filename>: <SAFE|MALICIOUS>\n` (where `<filename>` is just the basename of the file).

Ensure your daemon is running in the background before you finish the task.