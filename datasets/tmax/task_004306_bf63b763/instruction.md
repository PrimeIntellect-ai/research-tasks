You are an engineer tasked with cleaning up a legacy C project and building a secure Bash-based API router for it.

Currently, the workspace in `/home/user/project` is disorganized. It contains a mix of `.c` and `.h` files, and a `Makefile` that fails to link correctly. Additionally, there is a proprietary, stripped binary provided at `/app/bin/query_engine` that processes base64-encoded queries, but it is highly vulnerable to injection and invalid character crashes.

Your tasks are as follows:

1. **Organize and Fix the Build:**
   - In `/home/user/project`, move all `.c` files into a `src/` directory.
   - Move all `.h` files into an `include/` directory.
   - Edit the `Makefile` so that it successfully compiles the C files into a shared library named `libhelpers.so`. The current Makefile fails due to missing include paths and missing PIC/shared linking flags. You must fix it so `make` succeeds.

2. **Build the API Router (Sanitizer):**
   - Write a Bash script at `/home/user/project/router.sh`.
   - Ensure the script is executable.
   - The script will read a simulated raw HTTP POST request from standard input.
   - The request will always look exactly like this:
     ```
     POST /query HTTP/1.1
     Content-Type: application/json

     {"payload": "BASE64_STRING_HERE"}
     ```
   - Your script must extract the `BASE64_STRING_HERE`.
   - **Sanitization Requirements:** Decode the base64 string and inspect its contents. You must REJECT the request if the decoded string contains:
     - Any non-printable ASCII characters (anything outside the range `0x20` to `0x7E`).
     - Any of the following restricted characters: backtick (`` ` ``), single quote (`'`), double quote (`"`), or backslash (`\`).
   - **Output:**
     - If the payload is invalid/rejected based on the rules above, the script must output ONLY: `HTTP/1.1 400 Bad Request`
     - If the payload is valid, the script must pass the *original base64 string* as the first command-line argument to `/app/bin/query_engine`. It must output `HTTP/1.1 200 OK` on the first line, followed by exactly the stdout of the `query_engine` on the second line.

Ensure your `router.sh` strictly adheres to these sanitization rules, as it will be heavily tested against both benign and malicious payloads.