You are a database reliability engineer handling incident response. We have a situation where our automated backup logs might have been poisoned by an attacker trying to exfiltrate data under the guise of backup queries.

Your task has two parts:

Part 1: Video Forensic Analysis
We recorded the monitoring dashboard during the incident. The video file is located at `/app/dashboard.mp4`. 
Analyze the video to count exactly how many times the distinct alert "BACKUP IN PROGRESS" appears on screen. 
Write this integer count to `/home/user/backup_count.txt`. You can use `ffmpeg` and OCR tools (like `tesseract`, which you can install if needed) to extract and analyze frames.

Part 2: Adversarial Query Filter (Rust)
You must build a Rust command-line tool that acts as a log sanitiser/classifier to detect malicious data exfiltration disguised as backup queries. 
- A "clean" backup query typically dumps tables to our designated backup directory (`/mnt/backups/`) or uses standard `pg_dump` syntax.
- An "evil" query might attempt to dump data to unauthorized paths (e.g., `/tmp/`, `/var/www/`), use `UNION SELECT` to leak credentials, or use `COPY ... PROGRAM` to execute arbitrary shell commands.

Write a Rust project in `/home/user/query_filter/`. The compiled binary should be at `/home/user/query_filter/target/release/query_filter`.
Usage: `/home/user/query_filter/target/release/query_filter <path_to_query_log_file>`

- If the file contains ONLY clean backup queries, the tool must exit with status code `0`.
- If the file contains ANY malicious or unauthorized query patterns, the tool must exit with status code `1` (reject).

We have provided a sample of clean queries in `/app/corpus/clean/` and malicious queries in `/app/corpus/evil/` to help you tune your tool. Your tool will be evaluated against a hidden, much larger test set of both clean and evil queries using the exact same exit-code convention. You must perfectly preserve all clean logs and reject all evil logs.