You are an SRE tasked with restoring a corrupted monitoring pipeline and rewriting its core log parser.

We have a legacy secure backup script `/app/secure_restore.sh` that requires a passphrase to unlock the backup archive `/app/data.tar.gz`. The passphrase was left by the previous admin in an automated voicemail recording located at `/app/voicemail.wav`.

Your tasks:
1. Process the audio file `/app/voicemail.wav` to extract the spoken passphrase. (You may use tools like `ffmpeg` or download a small transcription tool like `whisper.cpp` to decode the audio).
2. Write an Expect script `/home/user/restore.exp` that automates running `/app/secure_restore.sh` and provides the transcribed passphrase when prompted. Running this script should extract the contents of the backup into `/home/user/restored_data/`.
3. Inside the restored data, you will find an executable named `oracle_parser` and a few sample log lines. The `oracle_parser` reads a single uptime log line from standard input and outputs a normalized JSON string.
4. The current `oracle_parser` is a black box compiled from a lost legacy language. Your main objective is to rewrite this parser in **Go**. Create `/home/user/uptime_parser.go` and compile it to `/home/user/uptime_parser`.
5. Your Go program must behave **bit-for-bit identically** to the `oracle_parser` for any given valid log line input over stdin. 
   - The input will always be a single line.
   - You must deduce the parsing logic, field names, and specific formatting rules (like how certain status levels might mutate the output) by experimenting with the `oracle_parser` using text processing tools.
   
Ensure your compiled binary is located at `/home/user/uptime_parser` and accepts input via standard input identically to the oracle.