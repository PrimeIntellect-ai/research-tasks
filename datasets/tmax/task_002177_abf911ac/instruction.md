You are an IT support technician resolving two escalated tickets.

**Ticket 1: Voicemail Transcription**
A user left an urgent voicemail regarding a server failure. The audio file is located at `/app/voicemail.wav`.
Listen to (or transcribe) the audio to extract the specific 4-character alphanumeric server error code the user mentions.
Write the exact 4-character code (in uppercase) to `/home/user/voicemail_code.txt`. 
You may install any command-line tools you need (like `ffmpeg`, `whisper-cpp`, etc.) to process the audio file.

**Ticket 2: Filename Sanitization Filter**
Our automated voicemail backup script frequently crashes or executes unintended commands because users upload files with spaces, newlines, and shell metacharacters in their names. 
We need a strict filename validator. 

Create a Bash script at `/home/user/validate_filename.sh`.
- The script must take exactly one argument: a filename (just the base name, not a full path).
- It must exit with code `0` (Success/Accept) if the filename is STRICTLY SAFE. A safe filename contains ONLY alphanumeric characters (A-Z, a-z, 0-9), dots (`.`), dashes (`-`), and underscores (`_`).
- It must exit with code `1` (Reject) if the filename contains ANY other characters (including spaces, quotes, newlines, glob characters, emojis, or control characters).
- The script must be robust against highly adversarial inputs (e.g., arguments starting with `-`, containing `$()`, or embedded newlines).
- Make sure the script is executable (`chmod +x`).

An automated test will run your script against two hidden corpora of filenames to ensure it accepts 100% of clean filenames and rejects 100% of malicious/problematic filenames.