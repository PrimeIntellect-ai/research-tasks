You are a network security engineer investigating suspicious activity on a Linux server. You have been provided with a network traffic capture log and the source code for a suspected rogue web service found on the machine.

Your objectives are:
1. **Traffic Analysis**: Inspect `/home/user/traffic_capture.txt` to identify the destination port the rogue service is listening on.
2. **Code Auditing & Vulnerability Analysis**: The rogue service's source code is located at `/home/user/rogue_service/src/main.rs`. Review the code to identify two major security vulnerabilities:
   - A Command Injection vulnerability.
   - A Cross-Site Scripting (XSS) vulnerability.
3. **Secure Coding & CSP Enforcement**: Modify `/home/user/rogue_service/src/main.rs` to fix these issues.
   - Fix the Command Injection vulnerability by properly passing arguments to the command without using a shell interpreter (`sh -c`).
   - Mitigate the XSS vulnerability by adding a strict Content Security Policy (CSP) header to the HTTP response. The header must be exactly: `Content-Security-Policy: default-src 'self'`
4. **Compile**: Ensure the modified Rust code compiles successfully by running `cargo check` in the `/home/user/rogue_service` directory.
5. **Reporting**: Create a JSON report at `/home/user/security_report.json` with the following exact structure:
```json
{
  "discovered_port": <integer_port_number>,
  "vulnerabilities": ["<CWE_ID_FOR_COMMAND_INJECTION>", "<CWE_ID_FOR_XSS>"],
  "csp_header_added": "<exact_csp_header_value>"
}
```
*Note: Use the standard CWE ID formats, e.g., "CWE-77" for Command Injection and "CWE-79" for XSS.*