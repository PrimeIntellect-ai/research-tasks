You are acting as a red-team operator crafting an evasion payload. We need to pass a secret authentication token to a local system service script without leaking the token in `/proc/[pid]/cmdline` (which happens if passed as an argument) or leaving it on disk. 

Your task is to write a C program that securely decodes a payload in memory and passes it to a target script via the environment.

Create a C program at `/home/user/stealth_auth.c` and compile it to `/home/user/stealth_auth` (ensure it is executable).

The program must perform the following operations:
1. Read exactly one line of text from Standard Input (`stdin`). This input will be a hex-encoded string (e.g., `0a1b2c`).
2. Decode this hex string into its raw byte representation in memory.
3. Decrypt the raw bytes using a single-byte XOR cipher with the key `0x7F`. The decrypted data is a null-terminated ASCII authentication token.
4. To prevent credential leakage via process arguments, you must securely pass this token to the target script using an environment variable. Set the environment variable `AUTH_TOKEN` to the decrypted string.
5. Use an `exec` family function (like `execle` or `execve`) to replace the current process image with the script located at `/home/user/login_simulator.sh`. Ensure the new environment containing `AUTH_TOKEN` is passed to the script, and do NOT pass the token as a command-line argument.

Note: The script `/home/user/login_simulator.sh` already exists on the system and will process the `AUTH_TOKEN` environment variable. 

Ensure your C code handles memory safely and compiles without errors using `gcc`.