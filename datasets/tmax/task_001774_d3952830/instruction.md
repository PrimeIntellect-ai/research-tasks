You are a security researcher analyzing a suspicious binary discovered in a compromised container. The stripped binary is located at `/app/suspicious_bin`. 

Initial analysis shows that the binary takes a string on standard input and outputs a single 32-bit hex string (e.g., `0x1a2b3c4d`). However, it has serious bugs: under heavy contention or with long inputs, it frequently deadlocks or produces non-deterministic outputs due to floating-point data races and numerical instability. 

Your goal is to:
1. Debug and trace the intermediate states of `/app/suspicious_bin` to reverse-engineer its exact hashing algorithm. (Hint: it uses a combination of integer bitwise operations and a chaotic floating-point sequence).
2. Write a bug-free, single-threaded equivalent program at `/home/user/clean_bin` (you may use Python, C++, or any language of your choice, but it must be executable via `/home/user/clean_bin <input_string>` or accept stdin). Ensure it has the correct permissions (`chmod +x`).
3. Your implementation must perfectly match the intended (deterministic) output of the original binary for any given input string.

The automated verification system will perform fuzz testing against your `/home/user/clean_bin` using thousands of random inputs and compare its output against a secure, bug-free reference oracle of the same algorithm.

Requirements for `/home/user/clean_bin`:
- Must read a single line of string from standard input.
- Must print the final computed hash as a zero-padded 8-character hex string prefixed with `0x` (e.g., `0x08a1b2c3`) to standard output.
- Must execute deterministically and avoid any deadlocks or uninitialized variable bugs present in the original binary.

Good luck.