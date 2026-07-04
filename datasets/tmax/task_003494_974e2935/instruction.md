You are a log analyst investigating a recent security incident. 

You have been provided with:
1. A directory of raw system logs in `/app/logs/` containing `auth.log`, `syslog`, and `access.log`.
2. An audio voicemail from the on-call engineer at `/app/voicemail.wav` who called in right when the attack started, mentioning the exact time they noticed the anomaly.

Your task:
1. Process the audio file `/app/voicemail.wav` to determine the exact time and date the engineer noticed the anomaly. (You may install and use open-source CLI tools like `openai-whisper` via pip to transcribe the audio).
2. Look in `/app/logs/auth.log` for a failed login attempt that occurred at that *exact* minute to identify the attacker's IP address.
3. Once you have the attacker's IP address, extract every log entry associated with this IP from *all* the log files in `/app/logs/`.
4. The logs have different timestamp formats. Normalize all extracted log entries so that the line starts with a Unix Epoch timestamp, followed by a space, followed by the original log message (excluding the original timestamp and hostname, just the process name and message).
5. Sort these normalized entries chronologically.
6. Save the final chronologically sorted and normalized log sequence to `/home/user/timeline.txt`.

Example output format for `/home/user/timeline.txt`:
```
1697152440 sshd[1234]: Failed password for invalid user admin from 192.168.1.50 port 54321 ssh2
1697152445 apache2: GET /admin_panel HTTP/1.1 404 192.168.1.50
```

Constraints:
- Use Bash and standard Linux tools (awk, sed, grep, date) for the data processing pipeline. 
- You will need to account for timezone differences if any, but assume all logs and the voicemail refer to the system local time (UTC).