You are a log analyst investigating a recent security incident in our voice-controlled industrial management system. We suspect an attacker used spoofed voice commands to trigger rapid, unauthorized state changes. 

Your objectives are to analyze an audio recording of the incident, extract the specific anomaly signature, and build a robust Python-based detector to filter future logs.

**Phase 1: Audio Analysis**
We have recovered a fragment of the attacker's audio artifact located at `/app/audio/override.wav`. You need to transcribe this audio file to extract the exact spoken override code (e.g., "BRAVO-NINER-2") and the incident time. 

**Phase 2: Build the Detector**
Create a Python script at `/home/user/detector.py` that acts as a log sanitization filter. 
1. It must take exactly one argument: the path to a plain-text log file.
2. The log files contain lines structured as: `[YYYY-MM-DD HH:MM:SS] USER_ID ACTION "TEXT_PAYLOAD"`
3. The detector must flag a log file as "EVIL" (reject) if it meets ANY of the following criteria:
   - Contains the exact override code extracted from the audio file within the text payload.
   - Exhibits rapid command bursting: More than 4 commands from the same `USER_ID` within any single 1-second time bucket (requires time-based bucketing and summary statistics).
   - Contains gaps in the log timestamps greater than 10 seconds followed immediately by a "SYSTEM_REBOOT" action (requires resampling and gap-filling analysis).
4. If the log file is safe, the script must exit with code `0`. If the log file is malicious, it must exit with code `1`.

**Phase 3: Validation against Corpora**
We have provided two datasets to test your detector:
- `/app/corpora/clean/`: Contains normal operational logs. Your script must accept all of these (exit code 0).
- `/app/corpora/evil/`: Contains known malicious logs. Your script must reject all of these (exit code 1).

Ensure your script handles standard imports efficiently and can be invoked from the command line exactly as: `python3 /home/user/detector.py <path_to_log_file>`. You may install Python packages like `openai-whisper` or `SpeechRecognition` to process the audio file.