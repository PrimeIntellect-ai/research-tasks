You are a network engineer assisting with a security audit of intercepted VoIP traffic. We have captured an audio payload from a suspicious connection, saved at `/app/voip_intercept.wav`. 

Your goal is to write a Go program (`/home/user/auditor.go`) that securely processes this audio, redacts sensitive information, and validates the logging server's certificate chain before saving the final report.

Here are the specific requirements for your Go program:

1. **Certificate Chain Validation:**
   Before processing the audio, your Go program must read and validate an X.509 certificate chain located in `/app/certs/`. The directory contains:
   - `/app/certs/root.pem` (The trusted Root CA)
   - `/app/certs/intermediate.pem` (The intermediate CA)
   - `/app/certs/server.pem` (The server certificate)
   Your program must programmatically verify that `server.pem` is valid and chains up to `root.pem` through `intermediate.pem`. If validation fails, the program must exit with a non-zero status code.

2. **Process Isolation (Sandboxing):**
   To securely transcribe the audio, your Go program must invoke a transcription tool (you may install and use the Python `openai-whisper` package, e.g., `whisper /app/voip_intercept.wav --model tiny --output_format txt --output_dir /home/user/`). 
   Because the audio file is untrusted, the Go program MUST invoke this transcription process inside a restrictive sandbox using `bwrap` (Bubblewrap). The sandbox must:
   - Unshare the network namespace (`--unshare-net`)
   - Mount the root filesystem as read-only (`--ro-bind / /`)
   - Provide standard `/dev` and `/proc` mounts
   - Mount a temporary filesystem on `/tmp`
   - Bind-mount `/home/user` as read-write so the transcript can be saved.

3. **Sensitive Data Redaction:**
   Once the transcription completes, your Go program must read the resulting text file. You must implement a redaction function in Go that uses regular expressions to find and replace the following with the exact string `[REDACTED]`:
   - Any valid IPv4 address (e.g., `192.168.1.50`).
   - Any 16-digit credit card number (continuous or separated by dashes/spaces).

4. **Output:**
   Save the final, redacted transcript to `/home/user/final_report.txt`. All text should remain identical to the transcription except for the replaced sensitive data.

Please write, compile, and run your Go program to produce `/home/user/final_report.txt`. You may install any necessary OS packages (like `bubblewrap`, `python3-pip`, `ffmpeg`) and Go modules to complete this task.