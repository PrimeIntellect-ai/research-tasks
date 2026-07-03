You are a security engineer tasked with rotating credentials for a legacy system. 

In your workspace at `/home/user/workspace`, there is a compiled legacy C++ authentication binary named `auth_service`. The source code for this binary has been lost, and the binary is considered potentially unsafe to run directly on the host network.

Your goal is to extract the master secret from this binary, generate a new access token for the upcoming rotation date, and verify the token by running the legacy binary in a sandboxed environment.

Here are the specific requirements:

1. **Reverse Engineering:** 
   Analyze the ELF binary `/home/user/workspace/auth_service` to extract the master secret key. The key is stored in the binary as a plaintext string prefixed with `SEC_KEY=`. Extract the value that follows the prefix.

2. **Token Generation (C++):**
   Write a C++ program at `/home/user/workspace/token_gen.cpp` that generates the new token. The program should accept two command-line arguments: the extracted secret key and a date string.
   The token generation algorithm must:
   - Iterate through each character of the secret key.
   - XOR each character of the secret key with the corresponding character of the date string (cycle through the date string if the secret key is longer).
   - Output the resulting bytes as a continuous lowercase hexadecimal string.
   
   Compile your program to `/home/user/workspace/token_gen` and generate the token using the extracted secret key and the target date string `"20241231"`.
   Save the resulting hexadecimal token to a file named `/home/user/workspace/new_token.txt`.

3. **Sandboxing and Verification:**
   The `auth_service` binary expects the token to be passed as its first command-line argument. Because this is an old, untrusted binary, you must test your generated token by running `auth_service` in a sandboxed process.
   Write a bash script at `/home/user/workspace/verify.sh` that uses the standard Linux `unshare` utility to run the binary. The binary must be run with its own isolated network namespace (`--net`) and isolated IPC namespace (`--ipc`). 
   The script should execute: `./auth_service <contents_of_new_token.txt>` inside the namespace.
   Make sure `verify.sh` is executable.

Ensure all requested files (`token_gen.cpp`, `new_token.txt`, and `verify.sh`) are present in `/home/user/workspace` with exactly those names.