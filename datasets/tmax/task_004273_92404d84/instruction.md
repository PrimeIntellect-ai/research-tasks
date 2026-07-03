You are an AI assistant helping a data scientist recover a lost data preprocessing pipeline.

We have a legacy compiled binary, `/app/cleaner_oracle`, which performs our initial dataset cleaning and feature scaling. We know it takes space-separated integers from Standard Input (one sequence per line) and applies a Min-Max scaling algorithm to normalize the features into an 8-bit integer range (0 to 255). 

Unfortunately, the original C source code was lost, and the binary is stripped. We need to recreate the exact logic in C so we can track experiments and integrate it into our new reproducible pipeline.

Your task:
1. Reverse-engineer or black-box test `/app/cleaner_oracle` to understand its exact transformation rules (pay close attention to how it handles rounding/truncation, and edge cases like all identical values).
2. Write a C program at `/home/user/cleaner.c` that replicates this behavior perfectly.
3. Compile your program to `/home/user/cleaner` (e.g., using `gcc -O3 /home/user/cleaner.c -o /home/user/cleaner`).

The automated verification system will feed thousands of random sequences of integers into both `/app/cleaner_oracle` and your `/home/user/cleaner` to ensure bit-exact equivalence on standard output.

Constraints:
- Your program must read line-by-line from `stdin` until EOF.
- It must output the processed space-separated integers to `stdout`, matching the oracle exactly.