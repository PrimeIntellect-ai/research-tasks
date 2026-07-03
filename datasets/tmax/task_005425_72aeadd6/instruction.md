You are a DevOps engineer stepping into an incident regarding our new C-based log ingestion pipeline. The previous developer, Dave, was working on a log sanitizer designed to filter out malicious payload injection attempts before they hit our database. Unfortunately, Dave abruptly left the company yesterday.

He left the source code in `/home/user/log_sanitizer`, but it currently fails to compile due to linker errors. Even when compiled with workarounds, we've noticed it either hangs indefinitely or crashes with a segmentation fault when processing certain logs. 

Before he left, Dave recorded a quick voice memo for the handover, which was automatically saved to `/app/voicemail.wav`. 

Your objectives are:
1. Extract the spoken contents of `/app/voicemail.wav` to uncover Dave's hints about the linker error and the logical bug. You may use any transcription tools or APIs you can access from the terminal (e.g., Python libraries, ffmpeg, or whisper.cpp if you install/compile them).
2. Fix the `Makefile` or source code based on the missing compilation flags or libraries mentioned in the audio.
3. Analyze `sanitizer.c` to identify and fix the infinite loop and/or infinite recursion bug. It is a parser that checks for nested malicious structures in the logs.
4. Ensure your compiled `/home/user/log_sanitizer/sanitizer` binary acts as a strict filter. When invoked as `./sanitizer <path_to_log_file>`:
   - It must exit with status code `0` for safe/clean logs.
   - It must exit with status code `1` for malicious or malformed logs (including those that previously caused hangs).

To help you test, Dave left a sample corpus in `/home/user/log_sanitizer/corpus/` with two subdirectories: `clean/` (which should all exit 0) and `evil/` (which should all exit 1). Note that the automated verification system will test your binary against a much larger, hidden evaluation corpus of clean and evil logs. 

Ensure your final compiled binary is located exactly at `/home/user/log_sanitizer/sanitizer`.