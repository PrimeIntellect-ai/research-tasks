You are a Site Reliability Engineer tasked with updating our health check and monitoring filters. 

Your manager has left an automated voicemail regarding a new routing and alerting rule for a specific service. The voicemail audio file is located at:
`/app/voicemail_SRE.wav`

Your task is to:
1. Listen to / transcribe the voicemail to extract the exact monitoring parameters and log formats.
2. Construct a Bash script located at `/home/user/log_filter.sh` that implements this filtering rule.
3. The script must read log entries from `stdin` and print the required output to `stdout`.
4. Ensure the script is executable (`chmod +x /home/user/log_filter.sh`).

The script must be written entirely in Bash (using standard coreutils like `awk`, `grep`, `sed`, or bash built-ins). It must accurately parse the standard input based on the rules dictated in the audio and output ONLY the precise fields requested, one per line.