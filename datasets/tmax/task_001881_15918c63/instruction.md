You are tasked with porting a legacy C audio processing tool into a minimal container environment. The tool, currently available as source code in `/home/user/src/audio_cleaner.c`, applies a proprietary noise-gating and phase-correction algorithm to raw audio. However, the original codebase was written hastily and suffers from multiple memory safety issues, undefined behaviors (such as uninitialized pointers and out-of-bounds buffer accesses), and it currently segfaults on modern systems.

Your objective has three parts:

1. **Memory Safety & Tool Compilation**
   - Refactor and debug `/home/user/src/audio_cleaner.c` to eliminate all memory leaks, segmentation faults, and undefined behaviors. 
   - The tool must read binary data from `stdin` and write the processed binary data to `stdout`. 
   - Write a `Makefile` in `/home/user/src/` that compiles the C file into an executable located exactly at `/home/user/bin/cleaner`. Ensure you use standard flags (e.g., `-O2 -Wall`).

2. **CI/CD Pipeline Script**
   - We need a local shell script simulating a CI/CD build step. Create `/home/user/ci_build.sh` (make sure it is executable). 
   - This script should automatically invoke your `Makefile`, verify that `/home/user/bin/cleaner` was successfully built, and run a simple test (e.g., processing `/dev/urandom` for a few bytes and ensuring exit code 0).

3. **Audio Transcription**
   - We have an artifact `/app/voicemail.wav` which is heavily corrupted by the specific noise profile that your tool is designed to remove.
   - Run your compiled tool to clean the audio: `cat /app/voicemail.wav | /home/user/bin/cleaner > /home/user/cleaned_voicemail.wav`.
   - Once cleaned, the audio contains a clear spoken phrase. Use whatever tools you prefer (you may need to install standard Linux transcription tools or utilities, e.g. whisper, if available, or upload/process locally) to recover the spoken content.
   - Write the exact transcript (in lowercase, stripped of punctuation) into `/home/user/transcript.txt`.

Note: Your compiled binary `/home/user/bin/cleaner` must behave EXACTLY like our reference implementation for any arbitrary input. Automated tests will subject your binary to intensive fuzzing against an oracle.