You are a DevSecOps engineer tasked with securing a legacy internal application. We have a compiled, stripped legacy microservice located at `/app/legacy_profile_svc`. This service handles user profiles and authentication, but we cannot modify its source code. We suspect it has a critical JWT validation vulnerability and leaks sensitive Personally Identifiable Information (PII).

Your objective is to execute a multi-stage security hardening workflow:

**Phase 1: Exploit Crafting & Vulnerability Demonstration**
1. Start the legacy service (it listens on `127.0.0.1:9000` by default when executed).
2. Analyze the binary or its behavior. It expects an `Authorization: Bearer <jwt>` header. We suspect it accepts tokens where the algorithm is set to "none" (unsecured). 
3. Craft an exploit: Create a forged JWT for the user `admin` using the `alg: none` vulnerability.
4. Save this forged raw JWT string to `/home/user/admin_exploit.jwt`. Ensure the file permissions are strictly set to `0600`.

**Phase 2: Policy-as-Code Proxy Implementation**
Since we cannot fix the legacy binary, you must write a Python-based security proxy to sit in front of it. 
1. Create a Python HTTP proxy listening on `127.0.0.1:8080`.
2. **Access Control (Policy Enforcement):** The proxy must intercept all incoming HTTP requests. It must inspect the JWT in the `Authorization` header. If the JWT header specifies `"alg": "none"` (or `"none"` in any case variation), the proxy must immediately reject the request with an HTTP `403 Forbidden` and NOT forward it to the legacy service. Valid signatures using other algorithms should be forwarded.
3. **Sensitive Data Redaction:** For requests that are allowed through, the proxy must inspect the JSON response from the legacy service. If the JSON payload contains the key `"ssn"`, the proxy must replace its value with exactly `"***-**-****"` before sending the response back to the client.
4. **Audit Logging:** Every rejected request must be logged to `/home/user/security_audit.log`. The log format must be exactly: `[REJECTED] IP:<client_ip> REASON:Insecure_JWT`. You must ensure that `/home/user/security_audit.log` is created with strictly `0600` permissions so only the file owner can read or write to it.

Ensure your Python proxy is running as a background service or daemon process so it can be tested. Write your code in `/home/user/sec_proxy.py` and execute it.