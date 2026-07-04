You are an AI assistant helping a data scientist clean up spectroscopy data for fitting molecular graph models.

We have acquired a dataset of 1024-point time-domain signals, but some of the signals contain anomalous high-frequency instrumental artifacts. These artifacts completely ruin our numerical integration and matrix decomposition routines later in the pipeline. 

We need to build a filter in C to reject the bad signals. We also need to use the `kissfft` library to perform the spectral analysis, which has been vendored on our system.

However, the vendored `kissfft` package at `/app/kissfft/` was accidentally modified by a previous intern and is currently broken. It compiles, but it seems to severely truncate or corrupt floating-point data during the FFT.

Your tasks:
1. Identify and fix the perturbation in the vendored `kissfft` library located at `/app/kissfft/`. The library should natively process single-precision floating-point values as intended by default.
2. Write a C program at `/home/user/filter.c` that compiles into an executable at `/home/user/filter`.
3. Your program should take a single command-line argument: the path to a text file containing 1024 float values (one per line, representing the time-domain signal).
4. The program must read the file, perform a 1024-point 1D Forward FFT using the fixed `kissfft` library, and compute the power spectrum (magnitude squared of the complex FFT output).
5. Detect the instrumental artifact: We define an "evil" (corrupted) signal as one where the power (magnitude squared) in any frequency bin from index 400 to 450 (inclusive) exceeds `50.0`. 
6. If the file is corrupted, the program must exit with return code `1` (reject).
7. If the file is clean, the program must exit with return code `0` (accept).

You can test your compiled filter against our sample datasets located at:
- `/app/corpus/clean/` (contains files that must be accepted)
- `/app/corpus/evil/` (contains files that must be rejected)

Compile your final executable to `/home/user/filter`. Do not hardcode the input paths; we will run your program against a hidden evaluation dataset using the signature `./filter <file_path>`.