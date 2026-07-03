You are a security auditor tasked with reviewing and exploiting permissions for a custom internal web server written in Rust. The server code and environment files are located in `/home/user/audit/`. You need to accomplish three specific objectives:

1. **Network Policy Configuration Audit**: 
   The server is protected by a network policy defined in `/home/user/audit/firewall_rules.json`. Analyze this file to determine which TCP port is allowed for the `internal_file_server` service. Write this integer port number to `/home/user/audit/open_port.txt`.

2. **Content Security Policy (CSP) Enforcement**:
   The web server source code is located at `/home/user/audit/server.rs`. It currently serves HTTP responses without any Content Security Policy. Modify `server.rs` so that every `200 OK` response includes the following HTTP header exactly:
   `Content-Security-Policy: default-src 'self'; script-src 'none';`
   Make sure not to break the existing response format (headers must be separated by `\r\n` and a blank line must precede the body).

3. **File Integrity Verification & Cryptanalysis**:
   The server validates a configuration file using a custom file integrity check before starting. The hash function, `weak_hash(data: &[u8]) -> u32`, is implemented inside `server.rs`. 
   The original valid configuration string is exactly `role=standard_user`. 
   Your task is to perform a pre-image / collision attack against this weak linear hash function. You must create a new file at `/home/user/audit/forged_config.txt` that meets the following criteria:
   - It must begin with the exact string `role=admin`
   - It must produce the *exact same 32-bit integer output* from `weak_hash` as the string `role=standard_user`.
   - You may append any printable or non-printable bytes after `role=admin` to achieve the collision.

Ensure all your final outputs (`open_port.txt`, `forged_config.txt`, and the modified `server.rs`) are saved in `/home/user/audit/`. Do not start the server, just leave the modified source code ready to be compiled.