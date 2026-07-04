You are an incident responder investigating a compromised web application stack. We suspect an attacker has planted a malicious binary that parses specific sensitive cookies to exfiltrate session data, and they are using a specific IP range to trigger this backdoor. 

Your investigation and remediation must proceed in the following stages:

**Stage 1: Multi-Service Configuration & Network Policy**
The application stack is located in `/app/`. It consists of an Nginx reverse proxy (listening on port 8080) and a Flask backend (on port 5000). 
1. Start the stack by running `/app/start.sh`.
2. Implement a network policy by modifying `/app/nginx/nginx.conf` to explicitly deny all HTTP traffic from the attacker's subnet: `192.168.200.0/24`. Ensure Nginx is reloaded with the new configuration so that requests from this subnet return a 403 Forbidden.

**Stage 2: Binary Analysis**
The attacker left behind a stripped ELF binary used for exfiltration at `/app/exfiltrator_bin`.
Analyze this ELF file. The attacker targets a specific cookie name. This cookie name is stored as a plaintext string in a custom ELF section named `.tgt_cookie`. Identify this exact cookie name.

**Stage 3: Sensitive Data Redaction (C implementation)**
To prevent further leaks while the backend is being patched, you must write a standalone HTTP header redaction tool in C. 
1. Create your C source file at `/home/user/redactor.c` and compile it to an executable at `/home/user/redactor`.
2. The program must read raw HTTP headers from `stdin` until EOF, and write the exact same headers to `stdout`, but with the target cookie's value redacted.
3. **Redaction Rules:**
   - Look for lines starting with `Cookie: ` or `Set-Cookie: ` (case-sensitive).
   - If the line contains the cookie name you found in Stage 2, followed immediately by an equals sign `=`, you must replace its value with the literal string `REDACTED`.
   - The value to be replaced ends at the first semicolon `;` or the carriage return `\r`, whichever comes first.
   - Example: If the secret cookie name is `SecretName`, and the input is `Cookie: other=123; SecretName=attackersession123; flag=0\r\n`, the output must be EXACTLY `Cookie: other=123; SecretName=REDACTED; flag=0\r\n`.
   - The rest of the stream must be reproduced bit-for-bit, unmodified.

Ensure your C program is highly robust against malformed input, buffer overflows, and missing newlines. We will rigorously test your compiled `/home/user/redactor` binary using a fuzz-equivalence verifier against our reference oracle.