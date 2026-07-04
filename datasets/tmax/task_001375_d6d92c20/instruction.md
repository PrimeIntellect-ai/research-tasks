You are an incident responder investigating a recent breach. The attackers exploited a proprietary log processing service. We have recovered the executable, located at `/app/log_processor`, but the source code is missing and the binary is stripped. 

We need you to accomplish two goals:
1. **Analyze the Binary**: Understand how `/app/log_processor` decodes incoming base64 payloads and identify the injection vulnerability it contains. The binary is an ELF executable that takes a base64 encoded string as a command-line argument and prints the decoded, processed log entry.
2. **Develop a Secure Replacement**: Write a secure replacement service in Python. Your service must listen for HTTP POST requests on `127.0.0.1:8080` at the endpoint `/process`. 
   - The request body will be JSON: `{"payload": "<base64_encoded_string>"}`.
   - Your service must decode the base64 payload, apply the same proprietary decoding logic as the original binary (which you must reverse-engineer), and then safely sanitize the output to prevent the injection/XSS vulnerabilities present in the original binary.
   - Specifically, you must HTML-encode the characters `<`, `>`, `&`, `'`, and `"` in the final processed string.
   - The response should be an HTTP 200 OK with JSON: `{"status": "success", "safe_log": "<sanitized_string>"}`.

Use standard bash utilities and Python to analyze the binary and write your secure service. Keep your service running in the background so our automated integration tests can verify it.