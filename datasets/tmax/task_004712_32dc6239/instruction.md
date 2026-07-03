You are a penetration tester and security developer working on an internal security auditing tool. You need to fix a broken vendored tool, integrate it, and expose its functionality securely via a dual-protocol gateway.

We have pre-vendored the source code for the directory brute-forcing tool `ffuf` (v2.0.0) at `/app/vendored/ffuf`. However, a junior developer introduced a deliberate perturbation in the code that prevents it from compiling.

Your objectives:

1. **Fix and Build the Vendored Package:**
   - Locate the source code in `/app/vendored/ffuf`.
   - Identify and fix the deliberate typo in `main.go` (a misspelled function call in the standard `flag` or initialization routines).
   - Build the binary using `go build -mod=vendor -o /home/user/ffuf_fixed` from within the directory.

2. **Develop the Security Gateway Service:**
   Create a Go application at `/home/user/sec_gateway.go` and run it. The service must run continuously and bind to two interfaces:
   
   **A. HTTP Interface (Port 8080):**
   - Listen on `0.0.0.0:8080`.
   - Expose an endpoint `GET /scan`.
   - When triggered, the handler must execute the `/home/user/ffuf_fixed` binary using Go's `os/exec` package. To ensure process isolation, you must configure the `Cmd.SysProcAttr` to run the process in a new PID namespace (e.g., using `syscall.CLONE_NEWPID` on Linux). 
   - Pass the arguments `-V` to the binary (which just prints the version).
   - Return the standard output of the command as the HTTP response body.

   **B. Secure TCP Interface (Port 8081):**
   - Listen on `0.0.0.0:8081` for raw TCP connections.
   - When a client connects, read a single line of input (up to the newline character).
   - The input will be a Hex-encoded, AES-256-CBC encrypted string.
   - Decrypt the payload using the following parameters:
     - Key: `0123456789abcdef0123456789abcdef` (32 bytes)
     - IV: `abcdef0123456789` (16 bytes)
     - Padding: PKCS7
   - If the decrypted string exactly equals `VERIFY_INTEGRITY`, perform a file integrity verification by calculating the SHA256 checksum of the `/home/user/ffuf_fixed` binary.
   - Send the resulting SHA256 checksum as a lowercase hex string (followed by a newline) back over the TCP connection and close the connection.
   - If the decrypted string is anything else, send "INVALID" and close the connection.

Ensure your Go application handles errors gracefully and continues running so the automated verifier can interact with both ports. Use only standard library packages for the Go application. Once the application is running, leave it running in the background.