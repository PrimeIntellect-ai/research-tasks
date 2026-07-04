You are a compliance analyst tasked with securing a vulnerable legacy authentication service. 

We have a proprietary, stripped binary located at `/app/legacy_auth`. This service listens on `0.0.0.0:8080` and handles HTTP authentication requests. A recent security audit discovered that when this binary receives an `Authorization` header containing shell metacharacters (specifically any of: `;`, `&`, `|`, `$`, or `` ` ``), it improperly spawns a background worker that leaks the raw credentials into its command-line arguments, making them briefly visible in `/proc` to any user on the system. Furthermore, it expects a `session_token` cookie to be present to validate the authentication flow.

Your objective is to implement a secure, high-performance C++ proxy and network policy to protect this binary without modifying it.

Perform the following steps:
1. **Network Firewall Configuration:** Use `iptables` to configure the firewall so that port `8080` is entirely blocked from external network interfaces, but remains accessible from `127.0.0.1`.
2. **Proxy Implementation:** Write a C++ program at `/home/user/audit_proxy.cpp` and compile it to `/home/user/audit_proxy`. This proxy must listen on `0.0.0.0:8000`.
3. **HTTP Header & Cookie Inspection:** For every incoming HTTP POST request to port `8000`, the proxy must:
   - Check for a `Cookie` header containing `session_token=`. If missing, the request must not be forwarded. The proxy must immediately return a `403 Forbidden` response.
   - Check the `Authorization` header. If it contains any of the dangerous shell characters (`;`, `&`, `|`, `$`, `` ` ``), the proxy must immediately return a `403 Forbidden` response.
   - If the request passes both checks, transparently forward the HTTP request to `127.0.0.1:8080`, read the service's response, and forward that response back to the client.
4. **Audit Logging:** Maintain a compliance audit trail at `/home/user/audit.log`. For every request processed, append a single line with the following format:
   `<Epoch Timestamp> <STATUS>`
   Where `<STATUS>` must be exactly one of: `BLOCKED_NO_COOKIE`, `BLOCKED_MALICIOUS`, or `ALLOWED_PROXIED`.

We will verify your solution by running a rigorous, automated traffic generation suite against your proxy on port 8000. Your proxy must successfully process a series of 500 interleaved legitimate and malicious HTTP requests with strict latency constraints.