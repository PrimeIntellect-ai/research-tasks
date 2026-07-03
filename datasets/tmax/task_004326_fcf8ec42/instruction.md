You are a monitoring specialist tasked with fixing and completing a deployment alerting pipeline. We have a legacy system that sends out emergency alerts as synthesized audio files, and a cron job that is supposed to parse these alerts, check our local disk quotas, and generate a final status report. However, the current setup is broken: the cron job fails to run properly due to PATH differences (it writes logs to the wrong place), and the core parsing script is missing.

Your objective is to complete the alerting pipeline by writing a Bash script that acts as the core parser and fixing the environment.

Step 1: The Audio Alert
There is an emergency audio alert located at `/app/emergency_alert.wav`. It contains a spoken transcription of a critical network connectivity failure and storage error code. Use the provided Whisper transcription tool located at `/usr/local/bin/whisper-cli` (already installed and available) to transcribe the audio file. Save the exact transcribed text to `/home/user/transcribed_alert.txt`.

Step 2: The Parsing Script
You must write a Bash script at `/home/user/parse_metrics.sh` that takes a continuous stream of system logs via `stdin`. The script must process these logs using text processing tools (`awk`, `sed`, `grep`) and perform the following operations:
1. Filter out any lines that do not contain the word "CRITICAL".
2. Extract the third column (which represents the process ID) from the remaining lines.
3. For each extracted process ID, append the exact storage error code you transcribed from the audio file (the last word in the transcription) separated by a dash.
4. Print the resulting strings to `stdout`, one per line.

Make sure your script at `/home/user/parse_metrics.sh` is executable. Our testing suite will fuzz your script by streaming thousands of randomly generated system logs into it and comparing its output *bit-for-bit* against our reference implementation.

Step 3: Connectivity and Quota Environment
We have a simulated mount point at `/home/user/mnt/data` (already created). You must write a wrapper script at `/home/user/run_alerts.sh` that:
1. Corrects the PATH environment variable so that standard system binaries (like `/bin` and `/usr/bin`) are prioritized.
2. Checks the disk usage of `/home/user/mnt/data` using `du -sh`.
3. Calls your `/home/user/parse_metrics.sh` script, piping in the file `/app/sample_logs.txt`.
4. Writes the final output to `/home/user/alert_output.log`, ensuring it doesn't write to the wrong location (as the old cron job did).

Do not use root privileges. Ensure all paths are absolute.