You are an operations engineer triaging an ongoing incident. A legacy, undocumented sensor data processor running in a containerized environment has been causing system panics. 

We have isolated the offending stripped binary at `/app/legacy_processor`. We also have the extracted crash logs from the container located at `/var/log/processor_crash.log`, which show the exact stack traces and the hex dumps of the corrupted inputs that caused the panics. 

Your task is to analyze the binary and the logs, and create a drop-in replacement script. 

Here is what you need to know and do:
1. **Container Debugging & Logs:** Inspect `/var/log/processor_crash.log` to understand what inputs the container was processing when it failed. 
2. **Corrupted Input Handling & Precision Loss:** Reverse-engineer `/app/legacy_processor`. The binary processes a binary file containing a stream of 32-bit floats. It performs a specific aggregation calculation. However, it handles corrupted/invalid byte sequences in a very specific (and undocumented) way, and the underlying mathematical operations suffer from measurable precision loss.
3. **Replication:** You must write a replacement program that takes exactly one argument (the path to an input binary file) and prints the resulting aggregated float to standard output. Your script must replicate the *exact* behavior of the legacy binary, including the precise floating-point precision loss and the exact logic used to skip or process corrupted inputs.
4. **Assertion Validation:** We strongly recommend you write intermediate test harnesses and use assertions to validate your script's outputs against the legacy binary's outputs across various edge cases before finalizing.

Save your final, fully working drop-in replacement at `/home/user/replacement.py`. You may use Python, or write a bash script wrapper around another language at that path. Ensure it has execute permissions. 

An automated fuzzer will invoke your script and the legacy binary with thousands of randomly generated inputs (mixing valid floats, NaNs, Infs, and completely random bytes) to ensure bit-exact equivalence of the standard output.