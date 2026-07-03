You are a storage administrator managing disk space for a legacy cluster. The cluster uses a custom Write-Ahead Log (WAL) binary format to track volume block allocations and deallocations. 

Unfortunately, the source code for the log processor was lost. All we have left is a stripped binary located at `/app/bin/wal_tracker`. 

This utility reads binary WAL records from `stdin`, updates an internal state of disk volumes, and prints state changes to `stdout` in a specific text format. It also handles basic error states when encountering invalid operations.

Your task is to reverse-engineer the behavior of `/app/bin/wal_tracker` and write a functionally identical C program. 

Requirements:
1. Analyze the binary `/app/bin/wal_tracker` using any tools available (e.g., `strace`, `xxd`, `objdump`, or by passing it custom inputs).
2. Write your C source code to `/home/user/my_tracker.c`.
3. Compile your program to an executable at `/home/user/my_tracker` (e.g., using `gcc -O2 /home/user/my_tracker.c -o /home/user/my_tracker`).
4. Your program must act as a drop-in replacement. It must read from `stdin` and write to `stdout`.
5. It must exactly match the original binary's `stdout` output and exit codes for ANY given input byte stream. 

An automated verification suite will randomly generate hundreds of raw binary streams (fuzzing) and pipe them into both your `/home/user/my_tracker` and the oracle `/app/bin/wal_tracker`. Your solution will only be marked correct if the stdout and exit codes are 100% bit-exact across all test cases.