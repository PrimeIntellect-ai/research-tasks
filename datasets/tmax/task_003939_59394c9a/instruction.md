You are a performance engineer tasked with debugging a data processing application. 

We have an audio recording from the lead engineer located at `/app/diagnostic_report.wav`. It contains spoken instructions detailing a sequence of filter weights that specifically trigger a severe statistical anomaly and memory crash in our new C-based audio filter.

The source code for the buggy filter is located at `/home/user/fir_filter.c`. This program is designed to read a continuous stream of raw 32-bit floats (little-endian) from standard input, apply a Finite Impulse Response (FIR) filter using weights provided as command-line arguments, and write the resulting 32-bit floats to standard output. 

Unfortunately, there is a bug in the ring buffer implementation that causes memory corruption and statistical anomalies (garbage outputs) when processing long streams, particularly noticeable when the circular buffer index goes below zero (hint: check how C handles the modulo operator `%` on negative numbers).

Your tasks:
1. Listen to / transcribe `/app/diagnostic_report.wav` to recover the hidden bug report and the exact integer filter weights mentioned.
2. Use interactive debugging (e.g., `gdb`) to trace the intermediate state and identify why the application is corrupting memory.
3. Fix the memory and performance bug in `/home/user/fir_filter.c`. The fixed program should correctly implement a standard FIR filter without reading out of bounds.
4. Compile your fixed version to exactly `/home/user/fixed_filter`.

The final executable must perfectly match the behavior of a standard, mathematically correct FIR filter for any arbitrary input stream of floats, but we will test it specifically with the weights extracted from the audio file.