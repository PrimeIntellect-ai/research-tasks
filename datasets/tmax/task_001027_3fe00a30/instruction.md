You are acting as a backup administrator archiving data. The senior sysadmin left you an audio recording with instructions for writing a highly specific differential backup manifest tool in C. 

Because our log rotation scripts often race with our writing processes, we rely on a fast snapshot-comparison tool rather than standard `rsync`. You need to create a C program that compares an old backup manifest with a dump of the current filesystem state to determine exactly which files need to be incrementally backed up, modified, or pruned.

Your tasks:
1. Locate and process the audio file located at `/app/voicemail.wav`. You may use any available tools (like `ffmpeg`, Python, or a transcription tool if you install one, though standard offline speech-to-text tools like `whisper-cli` or `pocketsphinx` can be installed via `apt`) to decode the spoken requirements.
2. Implement the C program according to the specific formatting, input/output rules, and edge cases detailed in the audio message. 
3. Write your source code to `/home/user/diff_tool.c`.
4. Compile your program to an executable at `/home/user/diff_tool` (using `gcc -O2 /home/user/diff_tool.c -o /home/user/diff_tool`).

The tool must be robust, as it will be heavily tested against random manifest permutations by our automated fuzzing integration suite. Ensure it correctly handles standard input and command-line arguments as dictated by the voicemail.