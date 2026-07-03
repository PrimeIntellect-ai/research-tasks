As a site administrator, you need to implement a custom disk quota monitoring system for user accounts, as standard quota tools are unavailable on this server. 

Your task is to create a C program that calculates directory sizes, and an automation script that applies this tool to all user directories and generates a health report.

Step 1: Write the C Program
Create a C program at `/home/user/src/quota_calc.c`.
- The program must accept exactly one command-line argument: the absolute path to a directory.
- It must recursively traverse the given directory and calculate the total size in bytes of all *regular files* within it (ignore directories and symlinks in the byte count, but you must traverse into subdirectories).
- The program should use standard POSIX libraries (e.g., `<dirent.h>`, `<sys/stat.h>`).
- If the total size of the regular files exceeds 10240 bytes (10 KB), the status is `EXCEEDED`. Otherwise, the status is `OK`.
- The program must print a single line to standard output in this exact format:
  `<directory_path> TOTAL_BYTES: <size> STATUS: <OK|EXCEEDED>`
  *(Example: `/home/user/users/alice TOTAL_BYTES: 4500 STATUS: OK`)*
- Compile this program to the executable `/home/user/bin/quota_calc`.

Step 2: Task Automation Script
Create a bash script at `/home/user/bin/run_checks.sh`.
- This script must iterate through all top-level subdirectories inside `/home/user/users/`.
- For each directory, it must execute `/home/user/bin/quota_calc` passing the absolute path of the user's directory.
- The script must capture the output of all these executions, sort the output lines alphabetically by directory path, and save the final sorted output to `/home/user/logs/quota_report.txt`.

Ensure your bash script has executable permissions. Once both the C program and the script are ready, execute `/home/user/bin/run_checks.sh` so that `/home/user/logs/quota_report.txt` is populated.