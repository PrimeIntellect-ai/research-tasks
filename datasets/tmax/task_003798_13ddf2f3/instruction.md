You are a research assistant organizing a dataset of acoustic telemetry. We have a recording of sonar telemetry in `/app/telemetry.wav`. The recording contains a sequence of pulses that represent a hidden state (either "tracking" or "searching").

Your task has three parts:
1. Extract the raw audio data from `/app/telemetry.wav` into an 8-bit unsigned PCM headerless format file at `/home/user/raw_audio.bin`. You must use standard shell tools (e.g., `ffmpeg` is installed).
2. Write a C program at `/home/user/bayesian_filter.c` that performs a discrete Bayesian update on a stream of 8-bit observations to estimate the probability of the "tracking" state. 
3. Compile your program to `/home/user/bayesian_filter` and process `raw_audio.bin` through it, saving the output to `/home/user/state_sequence.bin`.

### Bayesian Filter Specification
Your program must read a continuous stream of unsigned 8-bit integers from standard input (`stdin`) until EOF, and write unsigned 8-bit integers to standard output (`stdout`).

For each incoming byte (observation `x`), update the log-odds of the "tracking" state ($L$) using the following discrete rules to ensure perfect reproducibility across runs.

**Initialization:**
- Start with an initial log-odds $L = 0$ (represented as a 32-bit signed integer).

**Update Rule per byte `x`:**
- If $x < 64$, the evidence strongly suggests "searching". Subtract 2 from $L$.
- If $64 \le x \le 192$, the evidence is ambiguous. Add 0 to $L$.
- If $x > 192$, the evidence strongly suggests "tracking". Add 3 to $L$.

**Cap and Threshold:**
- To prevent integer overflow and provide bounds, after each update, cap $L$ such that $-10 \le L \le 10$.
- After applying the cap, output a single byte representing the predicted state:
  - If $L > 0$, output `1` (tracking).
  - If $L \le 0$, output `0` (searching).

**Pipeline Reproducibility:**
Ensure your C code is perfectly robust. It will be fuzzed against a reference implementation using completely random byte sequences to ensure the algorithmic state machine behaves identically to the oracle under all edge cases.