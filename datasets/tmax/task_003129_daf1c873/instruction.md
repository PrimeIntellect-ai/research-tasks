You are tasked with debugging and fixing a critical regression in a Go-based audio analysis tool called `audiostat`.

The repository is located at `/home/user/audiostat`. The tool analyzes audio files to detect statistical anomalies (e.g., sudden drop-offs in amplitude). 
Recently, a bug was introduced that causes the program to hang indefinitely when processing certain files. 

We have provided an audio file that triggers this hang at `/app/test_signal.wav`.

Your tasks are:
1. **Bisect the regression**: The `main` branch currently hangs on `/app/test_signal.wav`. The commit tagged `v1.0.0` (exactly 200 commits ago) is known to be good and processes the file successfully. Use `git bisect` to identify the exact commit that introduced the infinite loop.
2. **Fix the bug**: Inspect the bad commit. It introduced a loop termination bug in the statistical anomaly detection logic (likely a failure to advance a window pointer during a specific condition, such as absolute silence). Fix the Go code so that it correctly analyzes the file without hanging.
3. **Build the binary**: Compile your fixed code and place the resulting executable at `/home/user/audiostat_fixed`.

Your fixed binary must be functionally perfectly equivalent to our reference implementation. An automated fuzzer will test your `/home/user/audiostat_fixed` against hundreds of generated audio files to ensure identical output and exit codes. Do not change the CLI output format.