You are a backup administrator tasked with archiving surveillance data and sanitizing backup logs. We have a multi-stage archiving workflow that you need to implement.

Part 1: Video Archive Extraction
We have a surveillance video file located at `/app/surveillance.mp4`.
1. Use `ffmpeg` to extract one frame every second from this video.
2. Save these frames as JPEG images in the directory `/home/user/frames/` with the naming convention `frame_001.jpg`, `frame_002.jpg`, etc.
3. Count the total number of extracted frames and write this integer to `/home/user/frame_count.txt`.

Part 2: Log Sanitizer Implementation
You need to write a C program that sanitizes our compressed backup logs. The logs contain multi-line records. Some of these logs have been corrupted or contain malicious injection attempts (e.g., path traversal paths like `../` or `MALICIOUS` tags).
1. Write a C program at `/home/user/sanitize_logs.c` and compile it to `/home/user/sanitizer`.
2. The program must take two arguments: `INPUT_FILE` (a gzip-compressed log file `.log.gz`) and `OUTPUT_FILE` (an uncompressed text file).
3. The program must read the compressed stream directly (you may use `zlib.h`).
4. Parse the multi-line log records. Each valid record begins with `BEGIN_RECORD` on its own line and ends with `END_RECORD` on its own line.
5. Filter out any record that contains the substring `../` or `MALICIOUS` anywhere within its lines.
6. Write the allowed records to the `OUTPUT_FILE`. You **must** use an atomic write pattern: write the output to a temporary file (e.g., `OUTPUT_FILE.tmp`), flush/sync the data, and then atomically rename it to `OUTPUT_FILE`.
7. If the input file contains any malicious records, the program must exit with status code `1` (after writing the sanitized valid records). If all records are clean, exit with status code `0`.

Ensure your C code is robust and handles standard file operations safely. You may use shell commands to set up your environment or verify your compiled binary.