A critical DevOps pipeline failed overnight. The downstream log-processing shell script crashed entirely because it couldn't handle a severely malformed file path containing unexpected characters. To make matters worse, an automated cleanup job subsequently deleted the raw log files from the processing volume. 

Fortunately, we have two artifacts:
1. A video recording of the monitoring dashboard showing the terminal tailing the logs at the time of the crash: `/app/dashboard_record.mp4`.
2. A raw backup of the ext4 filesystem right after the deletion: `/app/log_volume.img`.

Your task is broken down into three parts:

**Part 1: Recovery and Timeline Reconstruction**
- Analyze the video `/app/dashboard_record.mp4` to determine the exact timestamp (format: `YYYY-MM-DD HH:MM:SS`) when the "FATAL: Shell parser exception" occurred.
- Recover the deleted log file from the ext4 image `/app/log_volume.img`. Extract the recovered file to `/home/user/recovered_system.log`.
- Find the log entry corresponding to the exact crash timestamp to identify the exact problematic file path that caused the crash. Write this exact file path to `/home/user/crash_cause.txt` (just the file path, no trailing newlines if possible).

**Part 2: Adversarial Sanitizer in C++**
To prevent this from happening again, we are rewriting the log filtering utility in C++.
- Write a C++ program at `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.
- The executable must take a single file path via standard input (stdin).
- It must reject (exit code 1) any input that contains shell metacharacters (such as `;&|*$<>()\`), unescaped spaces, or control characters (like newlines).
- It must accept (exit code 0) completely safe alphanumeric filenames (including underscores, dashes, and periods).
- Your compiled binary will be evaluated against a strict adversarial corpus. It must perfectly accept all safe inputs and strictly reject all malicious inputs designed to exploit the bash scripts.

**Deliverables:**
1. `/home/user/recovered_system.log` containing the recovered deleted logs.
2. `/home/user/crash_cause.txt` containing the exact payload that caused the crash.
3. `/home/user/sanitizer` (compiled from `/home/user/sanitizer.cpp`) meeting the strict adversarial filtering requirements.