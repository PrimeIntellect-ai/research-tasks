You are a penetration tester investigating a vulnerability in a custom TLS management daemon. The daemon improperly passes decryption keys via command-line arguments, which briefly become visible to any user via `/proc`. 

We have provided a screen recording of a terminal running a process monitor during the execution of this daemon: `/app/leak_capture.mp4`.

Additionally, we have recovered a directory containing 20,000 simulated process state dumps from a compromised environment: `/app/proc_dumps/`. Each file in this directory is a raw binary dump. The structure of each file starts with a mock ELF header, followed by various memory segments, one of which contains the command-line arguments.

Your task is to write a highly optimized C program (`/home/user/scanner.c`) to audit these files and uncover the scale of the leakage.

**Requirements:**
1. **Video Analysis**: Analyze `/app/leak_capture.mp4` to find the exact argument format used by the daemon to leak the key (it will look something like `--tls-key=...`).
2. **Scanner Implementation**: Write `/home/user/scanner.c`. It must:
    - Iterate over all 20,000 files in `/app/proc_dumps/`.
    - Parse the binary format to locate the command-line arguments. 
    - Extract the 32-character hexadecimal key from the argument.
    - Concatenate all extracted keys in alphanumeric order of the filename (e.g., `dump_00001.bin`, `dump_00002.bin`, etc.).
    - Compute the SHA-256 hash of the concatenated string.
3. **Process Isolation**: The dumped files are untrusted. Before parsing the files, your C program MUST sandbox itself using Linux `seccomp` (BPF filter) to explicitly deny the `execve`, `execveat`, `socket`, and `connect` system calls. 
4. **Output**: Your program must write the final SHA-256 hash (in hex format) to `/home/user/final_hash.txt`.

**Performance Constraints:**
Because this scanner will be deployed across millions of files in the production environment, your implementation must be highly efficient. The verifier will compile your code using `gcc -O3 /home/user/scanner.c -lssl -lcrypto -lseccomp -o /home/user/scanner` and execute it. Your program's execution time must be strictly less than **0.25 seconds** to process the 20,000 files.

You may use standard Linux shell commands (`ffmpeg`, `strings`, `grep`, etc.) to analyze the video and understand the binary format before writing your C program.