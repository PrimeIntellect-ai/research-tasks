You are acting as a penetration tester investigating a recent breach on a Linux server. The attacker compromised a legacy VoIP system and an authentication service. You have three primary objectives to complete your investigation and secure the system.

First, the attacker left behind an intercepted audio recording at `/app/voicemail.wav`. We believe this file contains the spoken secret keyword the attacker uses as a backdoor trigger in their malicious payloads. You need to transcribe or analyze this audio file to recover the exact secret keyword.

Second, the attacker exploited a vulnerability in a local authentication script located at `/app/auth_service.sh`. Analyze this script. You will find that it relies on insecure file permissions in the `/app/auth_keys/` directory to bypass standard authentication flows. You must identify exactly how the backdoor is triggered (which combines the keyword from the audio file and a specific pattern of failed/successful login attempts). 

Third, based on your findings, build an intrusion detection filter in Bash. Write a script at `/home/user/detect.sh` that takes a single file path as an argument. The script must analyze the provided log file (which follows a standard format of `TIMESTAMP IP USER ACTION PAYLOAD`) and classify it.
- If the log file contains the attacker's malicious auth flow or the backdoor trigger (derived from the audio and reverse engineering), output exactly `EVIL` to stdout and exit with code 1.
- If the log file represents normal traffic, output exactly `CLEAN` to stdout and exit with code 0.

Your script will be tested against two sets of log files:
- A clean corpus located at `/app/corpus/clean/`
- An evil corpus located at `/app/corpus/evil/`

Your script must accurately classify 100% of the files in both corpora. 
Make sure `/home/user/detect.sh` is executable. You may use any standard Linux tools (like `grep`, `awk`, `whisper.cpp` or `ffmpeg` if available) to accomplish this.