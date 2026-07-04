You are an infrastructure engineer diagnosing a failure in our custom network monitoring pipeline. The systemd service `net-monitor.service` has been crashing repeatedly. We suspect an ongoing attack injecting malformed payloads into our processing queue, accompanied by an anomalous event in our video surveillance stream.

Your task is to investigate the incident, build a robust filtering mechanism in C, and automate the cleanup.

**Part 1: Video Forensics**
We captured a video of the surveillance monitor during the time of the crash, located at `/app/incident.mp4`. Our initial analysis suggests the system drops the camera feed during network bursts, resulting in completely black frames.
1. Use `ffmpeg` (which is pre-installed) to analyze `/app/incident.mp4`.
2. Count the exact number of completely black frames (where all pixels are RGB 0,0,0).
3. Save this integer count to `/home/user/black_frames.txt`.

**Part 2: Payload Sanitizer (C)**
The pipeline crashes because the current packet analyzer lacks robust error handling for malformed HTTP-like metadata payloads. You need to write a standalone filter.
1. Write a C program at `/home/user/filter.c` and compile it to `/home/user/filter`.
2. The program must accept a single command-line argument: the path to a payload file (e.g., `./filter /path/to/payload.txt`).
3. The payload format consists of headers (each on a new line), a blank line (`\r\n\r\n` or `\n\n`), and a request body.
4. Your program must classify the file as "clean" (exit code `0`) or "evil" (exit code `1`).
5. A payload is "evil" if it meets ANY of the following criteria:
   - The `Content-Length` header value does NOT equal the actual byte length of the body.
   - The `User-Agent` header contains any of the following shell metacharacters: `$`, `|`, `;`, or `` ` ``.
6. A payload is "clean" if it has a matching `Content-Length` and a safe `User-Agent`. 
*(Note: Your solution will be tested against a hidden adversarial corpus of 100 clean and 100 evil files.)*

**Part 3: Automation**
1. Write a bash script at `/home/user/automation.sh` with execution permissions.
2. The script should iterate through all files in the directory `/app/incoming/` (which contains newly intercepted payloads).
3. Using your compiled `/home/user/filter`, evaluate each file.
4. Move all "clean" files to `/home/user/safe/` (create this directory if it doesn't exist).
5. Delete all "evil" files.
6. The script should be robust, handling files with spaces in their names.

Do not use external C libraries outside of the standard POSIX environment. Provide the correct exit codes in your C program, as our automated verification strictly relies on them.