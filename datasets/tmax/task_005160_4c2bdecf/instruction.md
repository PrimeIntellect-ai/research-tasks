You are a senior debugging engineer tasked with investigating a critical memory leak and crash in our long-running C++ audio transcription service. 

We recently experienced a catastrophic Out-Of-Memory (OOM) crash. The attackers exploited a vulnerability in our custom WAV parsing logic by submitting specially crafted audio files.

Here is what we have recovered:
1. `/app/last_request.wav`: The actual audio file processed right before the crash. Interestingly, the attacker left a voice message in this audio file explaining the "magic string" marker they injected into the heap.
2. `/app/service.core`: A partial memory dump (raw binary) of the service's heap at the time of the crash.
3. `/app/corpus/clean/`: A directory containing 50 valid, benign WAV files.
4. `/app/corpus/evil/`: A directory containing 50 malicious WAV files that trigger the unbounded memory allocation leak.

Your objectives:
**Step 1: Audio and Memory Dump Analysis**
Extract the spoken audio from `/app/last_request.wav` (you may install and use tools like `whisper` or `ffmpeg` to transcribe it). The transcript will reveal a specific uppercase "magic word" used as a marker.
Search the `/app/service.core` memory dump for this magic word. Immediately following this magic word in the dump is a 16-character hexadecimal payload. 
Write the magic word and the hex payload to `/home/user/leak_analysis.txt` in the format: `MAGIC_WORD:PAYLOAD`.

**Step 2: Fuzzing & Root Cause Analysis**
Analyze the headers of the files in the `clean` and `evil` corpora. The vulnerability is caused by a malformed chunk in the WAV file structure that tricks the C++ parser into allocating an enormous amount of heap memory before crashing. 

**Step 3: Adversarial Corpus Verifier (C++ Detector)**
Write a standalone C++ program at `/home/user/detector.cpp` and compile it to `/home/user/detector`.
This program must act as a sanitizer/filter for our API gateway. 
- It must take a single command-line argument: the path to a WAV file.
- It must parse the WAV file headers and determine if it is malicious (triggers the unbounded allocation) or benign.
- If the file is CLEAN, it must exit with status code `0`.
- If the file is EVIL, it must exit with status code `1`.

We will rigorously test `/home/user/detector` against the hidden test suites. It must achieve a 100% acceptance rate on the clean corpus and a 100% rejection rate on the evil corpus.