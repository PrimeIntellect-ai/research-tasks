You are a security auditor investigating a recent breach of our custom C-based web server. The incident response team left an audio voicemail detailing the attacker's actions. You need to identify the compromised asset, patch the vulnerability, and sanitize our compromised logs.

Follow these steps:
1. **Analyze the Voicemail:** 
   Listen to the incident report located at `/app/voicemail.wav`. We have installed `whisper.cpp` at `/opt/whisper.cpp/main` with the model `/opt/whisper.cpp/models/ggml-base.en.bin` for you to transcribe it. Identify the exact absolute file path the attacker managed to read/overwrite. Write ONLY this absolute path (e.g., `/var/log/messages`) to `/app/target.txt`.

2. **Fix the Path Traversal:**
   The web server source code is at `/app/server.c`. The function `int handle_upload(const char* filename, const char* content)` is susceptible to path traversal. Update `server.c` to reject the upload (return `-1` immediately without writing the file) if `filename` contains the substring `../` or starts with `/`. Otherwise, it should proceed normally. Compile your fixed version using `gcc -o /app/server_fixed /app/server.c`.

3. **Sensitive Data Redaction:**
   The attacker caused sensitive user data to be dumped into our server logs. Write a bash script `/app/redact.sh` that takes an input log file as its first argument (`$1`) and prints the redacted log to standard output. 
   Your script must:
   - Replace any 16-digit credit card numbers (format: 16 contiguous digits, or 4 blocks of 4 digits separated by hyphens) with the exact string `[REDACTED_CC]`.
   - Replace any password fields in query strings. For example, if the log contains `password=mySecret123&` or `password=mySecret123 ` (ending with a space or ampersand), it should be replaced with `password=[REDACTED]&` or `password=[REDACTED] `.

Ensure `/app/redact.sh` is executable.

We will verify your solution by running your `redact.sh` against a large, held-out log file and calculating the character-level similarity (metric: accuracy) compared to our golden standard. Your script must achieve an accuracy >= 0.95.