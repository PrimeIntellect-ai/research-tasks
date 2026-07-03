As a DevSecOps engineer, you are reviewing a legacy authentication component written in C. You have identified a critical security risk in `/home/user/auth_server.c`: it currently accepts a highly sensitive authentication token via a command-line argument (`argv[1]`), making it visible to all users on the system via `/proc/[pid]/cmdline` or the `ps` command.

Your task is to refactor `/home/user/auth_server.c` to securely handle the token. 

Please perform the following modifications to `/home/user/auth_server.c`:
1. Remove the usage of `argv[1]` for reading the token. The program should no longer expect any command-line arguments.
2. Read the token from the `AUTH_TOKEN` environment variable. The token provided in this environment variable will be Base64-encoded.
3. Immediately after extracting the value, call `unsetenv("AUTH_TOKEN")` to scrub it from the process environment, ensuring it does not leak into crash dumps, `/proc/[pid]/environ`, or child processes.
4. Base64-decode the extracted token. You must implement or include a basic Base64 decoding routine directly in the C file. Do not rely on external libraries (like OpenSSL or libb64) so that the program can be compiled simply with standard GCC.
5. Validate the decoded token by comparing it exactly to the hardcoded expected value: `"SuperSecretAppToken2024"`.
6. Depending on the validation:
   - If the decoded token matches, write the string `AUTH_SUCCESS` to `/home/user/auth_result.txt`.
   - If it does not match (or if the environment variable is missing), write `AUTH_FAILURE` to `/home/user/auth_result.txt`.
7. Once modified, compile your code to an executable at `/home/user/auth_server` using: `gcc /home/user/auth_server.c -o /home/user/auth_server`.

Ensure your C code handles potential errors gracefully (e.g., missing environment variable) by defaulting to `AUTH_FAILURE`. Do not print the token to standard output.