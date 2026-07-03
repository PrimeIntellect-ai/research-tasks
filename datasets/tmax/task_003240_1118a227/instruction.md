We have a C project located in `/home/user/telemetry_parser` that processes custom binary telemetry logs concurrently using pthreads. Recently, a regression was introduced somewhere in the last 200 commits: under heavy concurrent load, the parser occasionally drops records or deadlocks due to a race condition when threads handle partial reads.

Additionally, the current `HEAD` fails to correctly parse some new edge-cases in our binary format (e.g., zero-length records, or records with invalid checksums). 

We have provided a proprietary, stripped reference implementation binary at `/app/ref_parser` which correctly handles all edge cases and runs concurrently without race conditions.

Your objectives:
1. Diagnose the codebase in `/home/user/telemetry_parser`. You may want to write a minimal regression test in bash to trigger the race condition and optionally bisect the repository to find exactly when the concurrency bug was introduced.
2. Fix the concurrency bug (race condition / deadlock) in the latest `HEAD` without disabling threading. The processing must remain parallelized.
3. Fix the format parsing logic in the C code so that it correctly handles the edge cases. Its output must exactly match the output of `/app/ref_parser` when given the same binary log file.
4. Compile your fixed version and place the executable at `/home/user/fixed_parser`. 

The binary log format is passed as arguments to the program: `./fixed_parser <log_dir>`. The program prints JSON-lines to standard output. 

We will verify your solution by running `/home/user/fixed_parser` on a hidden validation directory of binary logs. To pass, your output must exactly match the reference binary's output, and it must complete execution in under 2.0 seconds (a strictly sequential fallback will timeout).