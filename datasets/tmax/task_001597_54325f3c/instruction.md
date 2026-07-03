You are a security researcher investigating a suspicious obfuscated binary found on a compromised Linux system. You have recovered two artifacts:
1. `/app/evidence.mp4`: A screen recording of the attacker's terminal. The attacker attempts to compile the original C source code, hits several compiler and linker errors, and then debugs a race condition in the multi-threaded payload encoder. The terminal output contains vital clues, including the hardcoded initialization vector (IV) and the exact locking mechanism that was causing the race condition (which affects the final byte permutation).
2. `/app/payload_encoder`: A stripped, obfuscated compiled version of the binary. 

Your objective is to reverse-engineer the encoding algorithm and write a pristine, bit-exact equivalent Python script at `/home/user/reconstruct.py`.

The Python script must accept a single command-line argument (a plaintext string) and print the encoded hex string to standard output, exactly matching the behavior of `/app/payload_encoder`.

Steps to succeed:
1. Analyze `/app/evidence.mp4`. Extract the frames (e.g., using `ffmpeg`) to read the attacker's terminal output. Identify the compiler/linker errors to understand the cryptographic primitives used, and read the GDB stack trace to find the hardcoded IV and understand how the race condition permutes the bytes.
2. Use assertion-based validation in your Python script to ensure intermediate states (like the IV initialization and the thread-chunking logic) match the constraints seen in the video.
3. Write the final Python script at `/home/user/reconstruct.py`. It must run natively (Python 3) without requiring compilation, simulating the exact same byte transformations (including the deterministic outcome of the "fixed" race condition). 

Output requirements:
- Create the executable script `/home/user/reconstruct.py`.
- It must take exactly one argument: `python3 /home/user/reconstruct.py <plaintext>`.
- It must print only the final uppercase hex string.