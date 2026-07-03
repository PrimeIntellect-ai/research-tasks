You are a DevSecOps engineer enforcing policy-as-code for a legacy internal service. 

There is a pre-compiled backend binary located at `/home/user/legacy_api` that is running on `http://127.0.0.1:8080`. 
Recent audits revealed that this binary contains a hardcoded backdoor administrative token embedded in its ELF `.rodata` or data sections. The token is stored in the format `BACKDOOR_TOKEN=<value>`.

Your objective is to write and deploy a secure Go-based reverse proxy that sits in front of this legacy application, enforcing strict security policies. 

Perform the following tasks:

1. **Binary Analysis**: Analyze the `/home/user/legacy_api` binary to extract the hardcoded backdoor token value. 

2. **TLS/SSL Setup**: The proxy must serve traffic securely. Generate a self-signed TLS certificate and private key. Save them as `/home/user/server.crt` and `/home/user/server.key`.

3. **Secure Proxy Implementation (Go)**:
   Write a Go reverse proxy at `/home/user/sec_proxy.go` that:
   * Listens on `https://127.0.0.1:8443` using the generated TLS certificates.
   * Forwards valid traffic to `http://127.0.0.1:8080`.
   * **Header/Cookie Inspection (WAF)**: Inspects incoming requests. If a request contains a cookie named `admin_token` that exactly matches the extracted backdoor token, the proxy must block the request and return an HTTP 403 Forbidden status code without forwarding it to the backend.
   * **Sensitive Data Redaction**: The proxy must log every incoming request to `/home/user/proxy.log`. Before logging, it must redact sensitive credentials. 
     - The `Authorization` header must be logged as `[REDACTED]` if present.
     - The value of the `session_id` cookie must be logged as `[REDACTED]` if present.
     - The exact log format appended for each request must be:
       `METHOD PATH | Auth: <Auth-Val> | Session: <Session-Val>`
       (If the header/cookie is entirely missing, output `NONE` instead of `[REDACTED]`).

4. **Deployment**:
   Build the proxy and leave it running in the background. Ensure the proxy successfully writes to `/home/user/proxy.log` when requests are made.

*Note: You may use standard Unix tools to analyze the binary and standard Go libraries for the proxy. Ensure the proxy is actively running on port 8443 when you finish.*