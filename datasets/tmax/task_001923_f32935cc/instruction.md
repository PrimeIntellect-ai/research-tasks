You are acting as a penetration tester investigating a suspected insider threat. We have intercepted an audio recording of the suspect, which contains critical intelligence about a covert channel they are using to embed malicious tokens within our SSH authentication logs.

Your objective is to build an intrusion detection script that can accurately identify these malicious logs without raising false alarms on legitimate traffic.

Step 1: Audio Analysis
An audio file has been recovered and placed at `/app/intercept_774.wav`. You need to transcribe or listen to this audio (you may use `whisper` or any installed audio processing tools like `ffmpeg` to extract or analyze it). The audio dictates the exact prefix and format of the malicious tokens injected by the APT group.

Step 2: Detector Implementation
Create an executable script at `/home/user/detector.sh`. 
This script must take exactly one argument: the absolute path to a log file.
Usage: `/home/user/detector.sh <path_to_logfile>`

The script must scan the provided file for the malicious token format identified from the audio.
- If the file contains one or more valid malicious tokens, the script must print exactly `EVIL` to standard output and exit.
- If the file does not contain any malicious tokens, the script must print exactly `CLEAN` to standard output and exit.

Step 3: Verification Against Corpora
To ensure your detector is accurate, we have provided two sets of training data:
- `/app/corpora/clean/`: Contains 100 legitimate SSH logs and logs with normal, safe authentication tokens.
- `/app/corpora/evil/`: Contains 100 SSH logs that have been compromised with the APT's backdoor token.

Your detector must successfully classify 100% of the files in the `clean` directory as `CLEAN` and 100% of the files in the `evil` directory as `EVIL`. 

Ensure your script handles standard bash scripting constructs efficiently and correctly parses the token structure (including any base64 constraints mentioned in the audio).