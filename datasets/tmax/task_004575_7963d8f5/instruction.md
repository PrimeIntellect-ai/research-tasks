You are a compliance analyst tasked with securing and generating audit trails for an internal compliance web system. The system consists of an Nginx reverse proxy, a Go-based Authentication service, and a pre-compiled Audit Report service. 

Currently, the system is offline due to a broken setup, and it has a known security vulnerability. You must fix the vulnerability, configure the certificates, run the services, and properly route the traffic.

All files are located in `/app/compliance_system/`.

**Step 1: Fix the Authentication Service Vulnerability**
The Go source code for the Authentication service is at `/app/compliance_system/auth/main.go`. It listens on `127.0.0.1:8081`. 
The `/login` endpoint takes a `redirect_to` query parameter, but it is vulnerable to an Open Redirect. 
Modify `main.go` to validate the `redirect_to` parameter. If the parameter contains an absolute URL (e.g., starts with `http://`, `https://`, or `//`), force the redirect to safely go to `/dashboard` instead. Relative paths (like `/settings`) should still be allowed. 
Compile the fixed service to `/app/compliance_system/auth/auth-svc` and start it in the background.

**Step 2: Fix the Certificate Chain**
The directory `/app/compliance_system/certs/` contains `leaf.crt`, `intermediate.crt`, and `server.key`. Nginx requires a complete certificate chain, but the current `server.crt` is missing or incomplete, causing chain validation to fail. Create a proper full-chain certificate file named `/app/compliance_system/certs/server.crt`.

**Step 3: Analyze and Start the Report Service**
There is a compiled ELF binary at `/app/compliance_system/report/report-bin`. We lost the documentation for this service, so we don't know what port it listens on. Analyze the binary to find its hardcoded listen port (it binds to `127.0.0.1`). Once you find it, start the service in the background.

**Step 4: Configure and Start Nginx**
Edit `/app/compliance_system/nginx.conf` to:
1. Listen on `127.0.0.1:8443` with SSL enabled, using the newly created `/app/compliance_system/certs/server.crt` and `server.key`.
2. Proxy requests for the path `/login` to the Auth service.
3. Proxy requests for the path `/audit` to the Report service (using the port you discovered).

Start Nginx using this configuration file. 

Leave all three services (Auth, Report, Nginx) running in the background. The automated verification system will issue HTTPS requests to `127.0.0.1:8443` to verify the TLS chain, test the open redirect fix, and pull the audit trail.