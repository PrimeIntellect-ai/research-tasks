We are investigating a severe memory leak and intermittent crashes in our long-running C-based audio feature extraction daemon. We suspect the issue is caused by malformed input files triggering a signed integer overflow when parsing chunk sizes, leading to corrupted memory allocations. 

A suspicious audio file was captured just before the last crash and has been saved to `/app/suspicious_recording.wav`.

Your task consists of two parts:

**Part 1: Intelligence Gathering**
Extract the spoken text from `/app/suspicious_recording.wav` to understand the context of the attack. You may use any available tools (like `ffmpeg`, `whisper`, etc.) to transcribe the audio. 
Save the exact transcription (lowercase, no punctuation) to `/home/user/transcript.txt`.

**Part 2: Adversarial Sanitizer**
We need you to build a robust input validator in C to protect our pipeline. 
1. Write a C program at `/home/user/wav_sanitizer.c` that parses standard RIFF/WAV headers. 
2. The program must detect integer overflow vulnerabilities (e.g., negative chunk sizes or sizes that overflow when padded) and corrupted inputs that our daemon might mishandle.
3. Compile it to an executable at `/home/user/wav_sanitizer`.

The sanitizer must operate as a CLI tool taking a single file path as its argument:
`./wav_sanitizer <path_to_wav_file>`

**Exit Status Requirements:**
*   Exit code `0`: The file is completely valid and safe to process.
*   Exit code `1`: The file is malformed, corrupted, or exploits an integer overflow.

To verify your sanitizer, it will be tested against two hidden corpora located in `/app/corpus/`:
*   `clean/`: Contains perfectly valid WAV files. Your tool must exit with `0` for all of these.
*   `evil/`: Contains malformed WAV files explicitly crafted with precision-loss and integer overflow exploits. Your tool must exit with `1` for all of these.

Ensure your C code relies on assertion-based validation and strict bounds checking to prevent precision loss or overflow during the parse phase.