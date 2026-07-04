You are a penetration tester building an automated exploit proxy for a Red Team engagement. Your task is to reverse engineer a target binary, discover its vulnerabilities, and write a C++ proxy service that automates the exploitation while enforcing strict access controls.

**Target Environment:**
There is a stripped, custom HTTP server binary located at `/app/vuln_uploader`. 
1. Start this binary in the background. It will automatically bind to `127.0.0.1:8081`.
2. The binary implements a rudimentary file download mechanism via the `/download?file=...` endpoint. 
3. It contains a path traversal vulnerability, but the endpoint is protected. You must reverse engineer the binary (using `strings`, `objdump`, or similar tools) to find the exact hardcoded `Cookie` required to access the endpoint.
4. There is a secret flag located at `/home/user/flag.txt`.

**Your Objective:**
Write and compile a C++ web server (your proxy) that listens on `127.0.0.1:9090`. You may download single-header libraries like `cpp-httplib` (`wget https://raw.githubusercontent.com/yhirose/cpp-httplib/master/httplib.h`) or use standard libraries.

Your C++ proxy must expose a `POST /exploit` endpoint that does the following:

1. **Authentication & HTTP Header Inspection:** 
   The request will contain an `X-Proxy-Auth` header. Reject the request with a `403 Forbidden` if this header does not exactly equal `RedTeamOps-2024`.
   
2. **Certificate Chain Validation:**
   The body of the `POST /exploit` request will contain a client certificate in PEM format. Your proxy must validate this certificate against a local Certificate Authority (CA) file located at `/home/user/ca.pem`. (You can write C++ code using the OpenSSL API, or securely invoke the `openssl verify` command via standard C++ system calls). If the certificate validation fails, return a `401 Unauthorized`.

3. **Exploitation:**
   If authentication and certificate validation succeed, your C++ proxy must automatically send an HTTP GET request to the vulnerable target (`127.0.0.1:8081`) to exploit the path traversal vulnerability and read `/home/user/flag.txt`. You must inject the hardcoded cookie you discovered during reverse engineering into this outbound request.

4. **File Permission and Access Control:**
   Once the proxy successfully retrieves the flag from the vulnerable server, it must save the flag to `/home/user/loot.txt`. Your C++ code must ensure that this file is created with strict `0400` (read-only by owner) permissions. Do not rely on `umask`; explicitly set the permissions in your C++ code.

5. **Response:**
   Finally, return an `HTTP 200 OK` response from your proxy containing the exact contents of the flag.

**Setup Instructions:**
The CA certificate `/home/user/ca.pem` and the target file `/home/user/flag.txt` already exist on the system. Compile your C++ server (e.g., `g++ server.cpp -o server -lssl -lcrypto`), start `/app/vuln_uploader`, and run your proxy server in the background. Leave both services running. An automated verifier will send HTTP requests to `127.0.0.1:9090` to evaluate your proxy.