You are a security auditor investigating a potential breach of a Go-based web service. The application files are located in `/home/user/service/`.

Your objective is to write a Go program at `/home/user/audit.go` that acts as an automated security scanner. When executed, your Go program must perform the following actions:

1. **Security Log Parsing**: Read the web server access log located at `/home/user/service/access.log`. Identify the single IP address that successfully submitted a Cross-Site Scripting (XSS) payload (look for the exact string `<script>` in the request URI). 
2. **Service Auditing**: Parse the source code of the web service located at `/home/user/service/server.go` to extract the integer port number the service is configured to listen on (look for the `http.ListenAndServe` function call).
3. **File Integrity Verification**: Compute the SHA-256 cryptographic hash of the compiled application binary located at `/home/user/service/server`. 

After extracting this information, your Go program must output the findings to a JSON file at `/home/user/audit_report.json`. 

The JSON file must strictly follow this exact structure:
```json
{
  "attacker_ip": "10.x.x.x",
  "listening_port": 1234,
  "binary_sha256": "abcdef1234567890..."
}
```

Constraints:
- You must write the solution in Go.
- Do not use any external dependencies outside the Go standard library.
- Make sure to run your Go program (`go run /home/user/audit.go`) so that the `/home/user/audit_report.json` file is generated and ready for verification.