You are a support engineer investigating a bug reported by a client. They have a time-calculation program that is outputting incorrect values and throwing silent environment warnings.

The client provided a diagnostic script (`/home/user/run_diag.sh`) and the C++ source code (`/home/user/calc.cpp`). 

When running `/home/user/run_diag.sh`, the "Exact Diff" calculation is losing precision (it seems to be rounding to whole numbers incorrectly instead of providing the exact fractional hours). Additionally, the client mentioned that the local hours being printed are completely wrong for UTC, and the program seems to be failing to load timezone data under the hood.

Your tasks are:
1. Use system call tracing (e.g., `strace`) to figure out what timezone file the program is vainly attempting to read, and fix the environment misconfiguration in `/home/user/run_diag.sh` so that it correctly uses the `UTC` timezone.
2. Identify and fix the precision loss bug in the formula implementation within `/home/user/calc.cpp` so that `Exact Diff` correctly outputs the fractional hour difference.
3. Once both the environment and the source code are fixed, execute `/home/user/run_diag.sh` and redirect its output to `/home/user/solution.txt`.

Ensure `/home/user/solution.txt` contains the precise, corrected output.