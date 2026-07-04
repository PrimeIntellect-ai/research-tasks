You are a penetration tester investigating a recent breach. The incident response team intercepted an audio voicemail left by one of the attackers, which contains crucial information about how they backdoored the company's internal PKI. 

The intercepted audio file is located at `/app/evidence/intercept.wav`.

Your task is to:
1. Transcribe or listen to the audio file to discover the exact criteria the attackers used for their malicious TLS certificates. You may install and use any Python libraries (e.g., `openai-whisper`, `SpeechRecognition`, `pocketsphinx`, or `ffmpeg` system tools) to extract the speech.
2. Based on the criteria spoken in the audio, write a Python script at `/home/user/cert_filter.py`. 
3. The script must accept a single command-line argument: the path to a directory containing PEM-encoded X.509 certificate files.
4. For each `.pem` file in the given directory, the script must evaluate it against the attacker's criteria.
5. The script must print exactly one line to standard output for each file in the format: `<filename> - CLEAN` or `<filename> - EVIL`. (e.g., `cert_01.pem - EVIL`).

The criteria involve inspecting the TLS certificate attributes, checking cryptographic signature algorithms, and validating file access permissions.

Ensure your Python script is robust, properly handles standard certificate parsing (you may use the `cryptography` package), and correctly applies all conditions mentioned in the voicemail.