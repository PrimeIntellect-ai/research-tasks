You are a performance engineer profiling a new scientific computing cluster. During a recent benchmarking run, the hardware performance counters occasionally generated corrupted data due to a firmware bug. 

The lead engineer investigated the issue and left an audio memo describing exactly how to identify these corrupted "evil" traces based on impossible physical invariants. You can find this memo at `/app/profiling_notes.wav`.

We have collected a large dataset of observational trace data. Your task is to build a C++ filtering tool to reshape our data pipeline by identifying and rejecting these corrupted traces.

Requirements:
1. Extract the anomaly conditions described in the audio file `/app/profiling_notes.wav`. You may use tools like `whisper` or `ffmpeg` (if available/installable in your environment) or write a quick script to transcribe it if needed, or simply play it if you have audio output configured. (Assume a transcription tool or method is at your disposal).
2. Write a C++ program at `/home/user/trace_filter.cpp` that reads a single trace CSV file. 
3. The CSV files have a header line and the following columns: `timestamp,instructions,cycles,l1_misses,l2_misses`.
4. Compile your program to an executable at `/home/user/trace_filter`.
5. Your executable must take exactly one command-line argument: the path to a CSV trace file.
    Example: `./trace_filter /path/to/trace.csv`
6. The program must return an exit code of `0` if the trace is entirely valid ("clean").
7. The program must return an exit code of `1` if the trace contains ANY rows matching the corruption conditions ("evil").

Ensure your C++ code is robust, correctly handles standard CSV formatting, and strictly adheres to the exit code requirements so it can be used in our automated experimental data environment.