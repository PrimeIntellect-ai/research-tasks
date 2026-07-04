You are a monitoring specialist dealing with a compromised alerting pipeline. Your system receives text-based monitoring logs and automated audio voicemail alerts. Recently, a misconfigured Docker compose network allowed external spam to flood the internal alerting directory alongside legitimate system logs.

You have two objectives:

1. **Audio Alert Routing**:
Listen to or transcribe the urgent voicemail alert located at `/app/urgent_alert.wav`. The audio contains the spoken name of the specific mailing list where critical alerts must be forwarded (e.g., if the audio says "forward to datacenter admins", the list name is `datacenter-admins`). 
Create a symbolic link at `/home/user/target_list` that points to the directory `/home/user/mail/<spoken_list_name>`. The destination directory should be created if it does not exist.

2. **Alert Sanitization Script**:
Write an idempotent Python script at `/home/user/alert_filter.py`. This script will act as a Git pre-receive hook classifier for our configuration repository, ensuring no spam logs are committed.
The script must take a single file path as a command-line argument.
It must read the contents of the file and print exactly `ACCEPT` to standard output if the file is a legitimate system monitoring alert, and exactly `REJECT` if the file is spam.
You can find samples of legitimate alerts in `/app/corpus/clean/` and samples of spam in `/app/corpus/evil/`. Inspect these directories to deduce the rules for classification (e.g., looking for specific required monitoring headers or forbidding spam keywords like promotional links).

Your script must be executable (`chmod +x /home/user/alert_filter.py`).