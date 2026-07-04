You are a compliance analyst generating an automated audit trail for a legacy internal service. We need to verify that we can recover access to the service and securely interact with it in an isolated environment.

You are provided with the source code of the legacy service at `/home/user/auth_server.go`. This service listens on port 8080 and expects a JSON payload containing a 4-digit PIN. 

Your task consists of two parts:

**Part 1: Cryptographic Recovery (Go)**
The system administrator lost the PIN for the audit account. We know the following:
* The PIN is exactly 4 digits (e.g., `0000` to `9999`).
* The server verifies the PIN by checking if the SHA-256 hash of the string `"audit_salt_" + PIN` matches the stored hash.
* The target SHA-256 hash is: `78ea7f858fa3914a844fcbfd70a41f6e2fde431522f1c84f686940a831e3d6e5`

Write a Go program at `/home/user/cracker.go` that brute-forces this hash to recover the 4-digit PIN. 

**Part 2: Process Isolation and Audit Trail (Bash)**
We cannot run the legacy service directly on the host network due to compliance rules. You must write a bash script at `/home/user/secure_audit.sh` that does the following:
1. Uses Linux namespaces to run the execution in an isolated environment (use `unshare -U -r -n` to map root and isolate the network).
2. Inside the isolated namespace:
   a. Brings up the loopback network interface (`lo`).
   b. Starts the legacy service (`go run /home/user/auth_server.go`) in the background.
   c. Waits briefly for the server to start.
   d. Uses `curl` to send a POST request to `http://127.0.0.1:8080/verify` with the JSON payload `{"pin": "<your_cracked_pin>"}`.
   e. Captures the JSON response from the server.

**Final Output Requirement**
Your `secure_audit.sh` script (or a combination of your Go program and bash script) must eventually produce a file at `/home/user/audit_trail.log` with exactly two lines:
Line 1: The 4-digit cracked PIN.
Line 2: The raw JSON response returned by the `curl` command (which contains the compliance token).

Ensure your script operates automatically when executed. You may test your code in the terminal to ensure the log file is correctly generated.