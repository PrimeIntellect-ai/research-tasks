We are migrating our systems and need to rotate the administrative credentials for a legacy web service. Unfortunately, the source code for this service has been lost, and the vendor no longer exists. 

The service is currently provided as a stripped Linux executable located at `/app/legacy_auth`. It acts as an HTTP server handling authentication and session management.

Your objective is to safely rotate the admin credentials and patch known vulnerabilities in this service without modifying the binary itself. You must accomplish this by writing a secure HTTP reverse proxy.

Here are your detailed requirements:

1. **Analyze the Legacy Binary:**
   - Execute or reverse-engineer `/app/legacy_auth` (tools like `strings`, `objdump`, `gdb`, or `strace` are available) to discover the port it listens on locally and the hardcoded administrative password it expects for the user `admin`.

2. **Build a Secure Reverse Proxy:**
   - Write a reverse proxy in the language of your choice that listens on `0.0.0.0:9000`.
   - The proxy must forward requests to the legacy service, but with the following modifications and security controls:
     
     **A. Credential Rotation:**
     When a client attempts to log in to your proxy via `POST /login` using the username `admin` and the **new** password `SuperSafeRotated99`, your proxy must intercept this and authenticate against the legacy service using the **old** hardcoded password you discovered. 
     If the client provides any password other than `SuperSafeRotated99`, the proxy should forward the request as-is (which should fail authentication at the backend).
     
     **B. Open Redirect Mitigation:**
     The legacy service has an open redirect vulnerability. When a login is successful, it reads a `redirect` query parameter (e.g., `/login?redirect=...`) and blindly echoes it into the `Location` header. 
     Your proxy must inspect the `redirect` parameter. If the parameter is an absolute URL (e.g., `http://evil.com` or `//evil.com`), the proxy must sanitize the final response by changing the `Location` header to `/dashboard`. If it is a valid relative path (e.g., `/settings`), it should be allowed.

     **C. Session Security Upgrades:**
     The legacy service sets a session cookie (e.g., `session_id=...`) upon successful login, but it lacks modern security attributes. Your proxy must intercept the `Set-Cookie` header from the legacy service and append `; Secure; HttpOnly; SameSite=Strict` to it before forwarding the response to the client.

3. **Deployment:**
   - Ensure both the `/app/legacy_auth` binary and your proxy script are running in the background.
   - The proxy must be bound to `0.0.0.0:9000` and be ready to accept incoming HTTP traffic.

Leave the proxy running when you are finished. An automated test will evaluate the proxy's behavior over HTTP.