You are a security researcher analyzing a suspicious Python script, `/home/user/suspicious_math.py`, which performs a complex sequence of mathematical operations on a given input file of integers. The script has been reported to crash under certain conditions when processing large inputs, but the exact mechanism is obfuscated.

Your goal is to investigate this crash by tracing the system calls, implementing a test minimization algorithm, and extracting the intermediate mathematical state just before the crash.

Perform the following tasks:

1. **System Call Tracing**: The script reads a hidden configuration file before performing its calculations. Use system call tracing to identify the absolute path of this hidden file. Write the absolute path to `/home/user/config_path.txt`.

2. **Delta Debugging / Test Minimization**: We have provided a large payload at `/home/user/large_payload.txt` that causes the script to crash with a `ZeroDivisionError`. You must write a Python script (e.g., using a Delta Debugging algorithm like `ddmin`) to reduce this payload to the absolute minimum sequence of lines that still reproduces the exact same crash. Save this minimized payload to `/home/user/minimal_crash.txt`. The minimized file must only contain the essential lines in their original relative order.

3. **Intermediate State Tracing**: Once you have the minimized payload, trace the internal state of the script. The script maintains an internal mathematical variable named `accumulator`. Determine the exact integer value of `accumulator` *immediately before* the crashing operation (the division by zero) is executed when running the script with your `minimal_crash.txt`. Write this integer value to `/home/user/accumulator_state.txt`.

Ensure all requested output files are created in `/home/user/` with the exact names specified.