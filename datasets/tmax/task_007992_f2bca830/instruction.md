You are a security researcher analyzing a suspicious C binary named `log_parser` that has been failing in production environments. You have a memory dump, a crashing input, and need to perform a complete analysis.

Your task has three phases:

**Phase 1: Memory Dump Analysis**
You have been provided with a memory dump file at `/home/user/malware.dmp`. We suspect it contains the obfuscated Command and Control (C2) domain.
1. The C2 domain in the dump is enclosed within a known plaintext wrapper format: `C2_START{` and `}`.
2. The domain string *inside* the braces is XOR-obfuscated using the single-byte key `0x42`. 
3. Extract the wrapper, isolate the obfuscated payload, decrypt it, and save the plaintext domain (just the domain, no braces or prefix) to `/home/user/c2.txt`.

**Phase 2: Delta Debugging & Minimization**
The binary `/home/user/log_parser` crashes with a Segmentation Fault (exit code 139) when processing the file `/home/user/trigger.log`.
1. Write a script (in bash, python, etc.) to perform delta debugging/minimization on `trigger.log`.
2. Find the absolute minimum contiguous byte sequence from `trigger.log` that still causes `/home/user/log_parser` to crash with a Segmentation Fault.
3. Save this exact minimal crashing byte sequence to `/home/user/minimal_crash.bin`.

**Phase 3: C Data Transformation**
Now that you know the exact byte sequence that triggers the crash, create a sanitizer.
1. Write a C program at `/home/user/sanitizer.c`.
2. The program must take two arguments: an input file path and an output file path.
3. It must read the input file, find any occurrence of the minimal crashing sequence (from Phase 2), and replace that exact sequence with four null bytes (`0x00 0x00 0x00 0x00`). All other data should remain unchanged.
4. Compile your program to `/home/user/sanitizer`.
5. Run your compiled program using `/home/user/minimal_crash.bin` as the input and `/home/user/safe_payload.bin` as the output.

Ensure all final files exist in `/home/user/` with exactly the names specified.