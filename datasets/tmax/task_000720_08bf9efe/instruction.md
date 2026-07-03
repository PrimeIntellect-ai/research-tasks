You are a Linux systems engineer responsible for hardening a local QEMU VNC management API service. 

An existing Go-based service located at `/home/user/workspace/vnc_manager.go` has a severe operational flaw: much like a misconfigured SSH daemon that silently drops connections instead of rejecting them cleanly, this API abruptly terminates the TCP connection if a specific security header is missing. Furthermore, the service requires strict environment configuration to run successfully.

Your task is to fix the application, correctly configure its deployment environment, and write a diagnostic tool to verify the fix.

Perform the following steps:

1. **Fix the Silent Drop**: 
   Examine `/home/user/workspace/vnc_manager.go`. You will notice that if the `X-VNC-Hardening` header does not equal `Strict`, the service hijacks the connection and abruptly closes it. 
   Modify the Go code so that instead of dropping the connection, it correctly responds with an HTTP `403 Forbidden` status code and the exact plain-text body `Hardening check failed`.

2. **Configure Service Deployment**:
   The service enforces a strict locale and timezone policy. It will fail to start or reject requests if the `TZ` environment variable is not `Asia/Tokyo` and the `VNC_PORT` is not defined.
   Write a bash script at `/home/user/workspace/deploy.sh` that:
   - Compiles `vnc_manager.go` into an executable named `vnc_manager`.
   - Exports the `TZ` environment variable as `Asia/Tokyo`.
   - Exports `VNC_PORT=8080`.
   - Starts the compiled `vnc_manager` executable in the background.
   Make sure `deploy.sh` is executable (`chmod +x`). Run this script so the service is active for step 3.

3. **Write a Connectivity Diagnostic Tool**:
   Create a Go script at `/home/user/workspace/diagnose.go`. This script must:
   - Make an HTTP GET request to `http://127.0.0.1:8080/status`.
   - Explicitly *omit* the `X-VNC-Hardening` header to trigger the behavior you just fixed.
   - Read the HTTP response.
   - Create a log file at `/home/user/workspace/audit.log` and write the result into it in the exact following format:
     `Result: {StatusCode} - {ResponseBody}`
     (For example: `Result: 403 - Hardening check failed`)

Ensure all files are placed exactly in `/home/user/workspace/`.