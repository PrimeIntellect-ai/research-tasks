You are a performance engineer tasked with debugging a set of bash scripts used for mathematical aggregation of system profiling data. The system consists of a local git repository located at `/home/user/perf_math` containing the scripts.

You have three main objectives:

**Phase 1: Regression Hunting (Git Bisection)**
The core math script, `calc_stats.sh`, calculates the integer variance of a list of numbers provided in a file. Recently, a commit introduced a bug where the script outputs completely incorrect variance calculations for certain datasets. 
The `HEAD` of the `main` branch is known to be broken. The commit tagged `v1.0` is known to be good.
1. Use git bisection to find the exact commit that introduced the bug. 
2. Write the full 40-character SHA-1 hash of the bad commit to `/home/user/bad_commit.txt`.

**Phase 2: Concurrency Debugging**
The wrapper script `/home/user/perf_math/aggregate_logs.sh` processes 50 chunked log files in the background and computes a global sum by reading and updating a shared file `global_sum.txt`. Because multiple background jobs read and write to this file simultaneously without synchronization, it suffers from a classic read-modify-write race condition, resulting in an incorrect final sum.
1. Debug and fix `/home/user/perf_math/aggregate_logs.sh` so that it safely computes the exact global sum of all chunks. You must use `flock` or another safe atomic Bash mechanism to prevent the race condition.
2. Run your fixed script. Save your fixed script to `/home/user/fixed_aggregate.sh`.
3. Save the correct final global sum to `/home/user/correct_sum.txt`.

**Phase 3: Fuzz Testing**
The `calc_stats.sh` script (even the version before the regression) has a hidden mathematical bug: it crashes with a "divide by zero" error under a specific statistical condition of the input data.
1. Write a fuzzing script in Bash that generates random datasets (files containing space-separated or newline-separated integers).
2. Feed these datasets into `/home/user/perf_math/calc_stats.sh` (using the `v1.0` version or a fixed version) until you trigger the bash divide-by-zero error.
3. Once found, save the exact input data that caused the crash into `/home/user/crash_input.txt`.

Requirements:
- Only standard Linux CLI tools and Bash built-ins are allowed. 
- Do not use Python, Perl, or other scripting languages.
- Ensure all output files are placed exactly as requested.