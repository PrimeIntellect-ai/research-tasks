You are a storage administrator responsible for managing disk space and securing your organization's automated backup pipeline. Recently, an attacker infiltrated the network and began corrupting configuration files and storage archives by injecting a specific malicious byte payload. 

Your task is to build a high-performance C-based stream filter to sit in the backup pipeline. This filter will process files via standard standard streams (stdin to stdout), blocking malicious files from entering the incremental backup pool while perfectly preserving clean files.

**Step 1: Incident Forensics (Video Analysis)**
The security team captured a screen recording of the attacker's terminal session during the breach. The video is located at `/app/evidence.mp4`.
1. Use `ffmpeg` (preinstalled) to extract the frames from this video.
2. Analyze the frames to find the exact 16-byte ASCII signature the attacker injected into the files. It will be clearly visible in one of the terminal commands shown on screen.

**Step 2: Configuration Interpretation**
Read the backup pipeline configuration file at `/app/backup.conf`. This file specifies a mandatory `BUFFER_SIZE` parameter. 

**Step 3: Develop the Stream Filter (C Programming)**
Write a C program at `/home/user/stream_filter.c` and compile it to `/home/user/stream_filter`. 
Your program must:
1. Read binary data from standard input (`stdin`) and write safe data to standard output (`stdout`).
2. Read the input strictly in chunks equal to the `BUFFER_SIZE` specified in `/app/backup.conf`.
3. Analyze the stream for the 16-byte malicious signature identified in Step 1. 
4. **Crucial:** The signature might be split across two consecutive buffer reads. Your program must correctly detect the signature even if it spans a chunk boundary.
5. If the signature is detected at any point in the stream, the program must immediately terminate, outputting nothing further, and return exit code `1` (Reject).
6. If the entire file is processed and the signature is never found, the program must have written the exact, unmodified contents of the input file to `stdout`, and return exit code `0` (Accept).

**Step 4: Iterative Testing against the Corpora**
The security team has provided two sets of files to test your filter:
*   A "clean" corpus located in `/app/corpus/clean/`
*   An "evil" corpus located in `/app/corpus/evil/`

You must test your compiled `/home/user/stream_filter` against these directories. Ensure your filter correctly accepts all clean files (preserving their contents perfectly via stdout) and rejects all evil files (exit code 1).

Complete the implementation and verify it works against the corpora. Ensure the final compiled executable remains at `/home/user/stream_filter`.