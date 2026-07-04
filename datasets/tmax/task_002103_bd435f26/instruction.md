You are acting as a support engineer collecting diagnostics and fixing a critical issue in a text parsing utility. A customer has reported that our C-based parser occasionally hangs infinitely on certain inputs. 

Your task is to minimize the failing test case, fix the bug, and create a statistical regression test to ensure it is fully resolved.

Here is your environment:
- The buggy C source code is located at `/home/user/parser.c`.
- The compiled binary is at `/home/user/parser`.
- The customer provided a large text file that triggers the hang, located at `/home/user/crash_input.txt`.

Perform the following steps:
1. **Delta Debugging / Test Minimization**: Identify the absolute shortest contiguous substring from `/home/user/crash_input.txt` that still causes the `/home/user/parser` binary to hang (run for more than 1 second). Save this exact minimized string into a new file called `/home/user/minimized_crash.txt` (no trailing newlines unless they are part of the minimal crash string).
2. **Loop Termination Fix**: Investigate `/home/user/parser.c`. Identify the cause of the infinite loop, fix the logic (do not remove the feature, just fix the loop termination), and recompile the binary to `/home/user/parser`.
3. **Statistical Regression Test**: Write a bash script at `/home/user/test_runner.sh` that acts as a fuzzer. It should:
   - Generate 1000 random strings, each 20 characters long, containing a random mix of the characters `[`, `]`, and `*`.
   - Run the newly compiled `/home/user/parser` against each string, passing the string as the first command-line argument.
   - Enforce a 1-second timeout per run.
   - Count how many runs hit the timeout (hang).
   - Write the final result to `/home/user/stats.log` in exactly this format: `Timeout Failures: X` (where X is the number of timeouts).

Make sure all files have appropriate execution permissions where necessary.