You are a network security engineer tasked with incident response and remediation. We recently discovered an undocumented, stripped binary running on our internal network at `/app/upload_server_bin`. This binary acts as a custom file upload service, but our traffic inspection revealed it is susceptible to a severe path traversal vulnerability. Furthermore, it uses a proprietary encryption scheme for its payloads and a custom authentication token mechanism, bypassing our standard security proxies.

Your objective is to reverse-engineer the behavior of this binary and implement a secure replacement in Python that acts as an application-level firewall and upload handler. 

Here are your specific requirements:

1. **Analyze the Binary**: 
   Investigate `/app/upload_server_bin` to determine how it validates authentication tokens in the `X-Custom-Auth` header and how it decrypts the incoming file payloads. You can treat the binary as a black-box oracle or reverse-engineer it using tools like `strings`, `objdump`, or `gdb`. 

2. **Implement an Application-Level Firewall & Handler**:
   Write a Python web service that listens on `127.0.0.1:8443` (HTTP protocol). This service must replace the insecure binary.
   - **Authentication Testing**: Your service must only accept requests that have a valid `X-Custom-Auth` header based on the logic you extracted from the binary.
   - **Decryption**: It must decrypt the incoming payload using the algorithm and key hardcoded in the binary.
   - **Network Policy / Filtering**: Implement an application-level firewall rule that strictly rejects any request where the target filename (provided in the `X-File-Name` header) contains path traversal sequences (e.g., `../`, `..%2F`, or absolute paths outside the designated upload directory).
   - **Secure Upload**: Valid, decrypted files should be saved securely to `/home/user/safe_uploads/`.

3. **Logging**:
   For every request processed, append a JSON line to `/home/user/firewall_access.log` with the keys: `status` ("ACCEPTED" or "REJECTED"), `filename` (the requested file name), and `reason` (e.g., "Invalid Auth", "Path Traversal Blocked", "Success").

Keep your Python service running in the background. Automated verification will connect to `127.0.0.1:8443` using various payloads, auth tokens, and path traversal attempts to ensure your implementation securely handles the traffic and successfully replicates the custom encryption/auth logic without the vulnerability.