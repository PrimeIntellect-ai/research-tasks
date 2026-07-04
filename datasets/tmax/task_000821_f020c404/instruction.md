You are a penetration tester analyzing a proprietary token generation and validation service. You have acquired two artifacts from a compromised sandbox environment:
1. `/app/debug_session.mp4`: A screen recording of the server's debug console during startup. 
2. `/app/token_checker`: A stripped, dynamically-linked x86_64 ELF binary that the server uses to validate HTTP cookies and generate process isolation tokens.

Your objective is to reverse-engineer the token derivation algorithm and write an equivalent C implementation. 

### Step 1: Analyze the Video
The video `debug_session.mp4` contains scrolling text of the server's initialization. During this process, the server prints a configuration line containing `SERVER_SEED: ` followed by a hexadecimal byte. You must extract this seed, as it is used in the hashing algorithm. (ffmpeg is preinstalled if you need to extract frames).

### Step 2: Reverse Engineer the Binary
Analyze the `/app/token_checker` binary. 
- It takes exactly one command-line argument: an HTTP Cookie header string (e.g., `Cookie: theme=dark; SessionId=1234abcd; lang=en`).
- It extracts the value of the `SessionId` cookie (which consists of hex characters).
- If the `SessionId` cookie is missing or malformed, it outputs `ERROR: Invalid SessionId` to stdout and exits with code 1.
- If valid, it combines the parsed hex bytes with the `SERVER_SEED` using a custom algorithm, applies a bitwise transformation, and outputs the resulting token in hex format to stdout (e.g., `TOKEN: 8f2c...`), exiting with code 0.

### Step 3: Implement the Clone
Write a C program at `/home/user/my_token_checker.c` and compile it to `/home/user/my_token_checker`. 
Your program must be a **bit-exact equivalent** of `/app/token_checker`. For any given input string provided as `argv[1]`, your binary must produce the exact same standard output, standard error, and exit code as the oracle binary. 

Do not rely on calling the original binary from your C code, as your binary will be tested in an environment where the original binary is removed. 

**Constraints:**
- Use C as your primary language.
- The compiled executable must be placed at `/home/user/my_token_checker`.
- Ensure you handle edge cases (e.g., no arguments provided, no `SessionId` found, invalid characters in the token) exactly as the original binary does.