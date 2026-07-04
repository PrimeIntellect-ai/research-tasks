You are a script developer tasked with creating a secure Bash-based proxy utility to protect a legacy backend emulator. The legacy backend (`/home/user/legacy_backend`) has known C/C++ memory safety vulnerabilities (specifically, a buffer overflow when given payloads longer than 20 characters) and lacks rate limiting. 

Your task is to write a Bash script at `/home/user/secure_proxy.sh` that reads commands from standard input (stdin) line-by-line, performs request validation, enforces rate limiting, acts as a partial interpreter, and passes safe commands to the backend.

Implement the following logic in `/home/user/secure_proxy.sh`:

1.  **Read Loop:** Read lines from stdin continuously until EOF.
2.  **Rate Limiting:** Allow a maximum of 3 commands (of any type) per second. Use the current Unix timestamp (`date +%s`) to track the 1-second windows. If a command exceeds this limit within the same second, do not process it and print exactly: `ERR: RATE_LIMIT`
3.  **Local Interpreter:** 
    *   If the command is exactly `PING`, do not send it to the backend. Instead, print exactly: `PONG` (This counts towards the rate limit).
4.  **Memory Safety Validation:**
    *   If the command starts with `EXEC ` (e.g., `EXEC some_payload`), calculate the length of the payload (the string after `EXEC `). 
    *   If the payload length is strictly greater than 20 characters, drop the request to prevent undefined behavior in the C backend, and print exactly: `ERR: MEM_SAFETY`
5.  **Backend Pass-through:**
    *   If an `EXEC ` command is 20 characters or fewer, pass the entire line (including `EXEC `) to the backend utility by running: `/home/user/legacy_backend "<line>"`
    *   Print the standard output of the backend directly.
6.  **Unknown Commands:**
    *   For any command that is not `PING` and does not start with `EXEC `, print exactly: `ERR: INVALID_REQ` (This also counts towards the rate limit).

Ensure your script is executable (`chmod +x /home/user/secure_proxy.sh`). Use only standard Bash built-ins and coreutils.