You are taking over a legacy codebase for acoustic anomaly detection. We are migrating away from an old compiled C binary to a pure Python implementation for easier maintenance. 

The original binary is located at `/app/legacy_detector`. 
A previous developer started the port, and their incomplete script is located at `/home/user/detector.py`. 

The Python script mostly works but fails to produce the exact same bit-level output as the legacy binary. We suspect the issues fall into a few categories:
1. Floating-point vs fixed-point precision differences (the C binary was optimized for a microcontroller with specific integer-math quirks).
2. Off-by-one errors in how the audio sliding windows are chunked or padded.

Your task is to debug, reverse-engineer, and fix `/home/user/detector.py` so that its standard output is **100% bit-exact equivalent** to `/app/legacy_detector` for *any* valid 16-bit Mono PCM WAV file. 

**Resources Provided:**
- The oracle binary: `/app/legacy_detector <path_to_wav>`
- The buggy Python port: `python3 /home/user/detector.py <path_to_wav>`
- A test audio fixture: `/app/sample_audio.wav` (Use this for initial debugging, diff analysis, and memory inspection).

**Expected Output:**
- The script `/home/user/detector.py` must be modified in-place.
- It must take exactly one argument (the path to the WAV file).
- It must print a series of space-separated integer values to `stdout` (exactly matching the binary's output format). 

Use interactive debuggers, diff tools, or binary analysis tools (like `objdump` or `ghidra` if needed) to figure out exactly how the legacy binary computes its windowed energies and fix the Python logic.