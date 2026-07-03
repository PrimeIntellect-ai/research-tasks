You are a network engineer investigating an intercepted VoIP communication and a subsequent data exfiltration attempt. We have recovered several artifacts from the compromised network segment.

Your objective is to build a log sanitizer to prevent sensitive data from leaking in our network telemetry. To build this sanitizer correctly, you must extract the sensitive terms and patterns by analyzing the recovered artifacts.

First, analyze the intercepted VoIP audio recording located at `/app/intercepted_voip.wav`. You will need to transcribe this audio (tools like `whisper` or `ffmpeg` are available in the environment) to discover the top-secret operation codename spoken by the threat actor. This codename is highly sensitive and must be redacted from all text logs.

Second, the attacker left behind a compiled Python script at `/app/cert_validator.pyc` which they used to pin a rogue TLS/SSL certificate. Reverse engineer or disassemble this bytecode. Inside, you will find:
1. The expected CN (Common Name) of the rogue TLS certificate they used.
2. A specific regular expression pattern the attacker used to scrape authentication tokens from our traffic. 

Finally, implement the log sanitizer. Create a Python script at `/home/user/log_sanitizer.py`. Your script must accept two arguments: an input directory containing `.log` text files, and an output directory.
`python3 /home/user/log_sanitizer.py <input_dir> <output_dir>`

Your script must read each file from `<input_dir>`, and write the processed version to `<output_dir>` with the exact same filename.
The sanitizer must:
- Replace any instance of the top-secret operation codename (found in the audio) with the exact string `[REDACTED_CODENAME]` (case-insensitive match, but preserve the rest of the text).
- Replace any text matching the authentication token regular expression (found in the `.pyc` file) with the exact string `[REDACTED_TOKEN]`.
- Replace any instance of the rogue TLS certificate's Common Name (found in the `.pyc` file) with the exact string `[REDACTED_TLS_CN]`.

If a log file contains none of these sensitive elements, it must be copied to the output directory entirely unchanged. 
We will grade your script using an automated test suite against two hidden directories containing real network logs.