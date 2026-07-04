You are acting as a compliance analyst generating an audit trail for an internal web service. We need to secure an existing Go-based web service located at `/home/user/app/server.go` before it can be certified.

Your objectives are to audit the service, identify its cryptographic vulnerabilities, patch it to enforce a Content Security Policy (CSP), and create a sandboxed execution script.

Perform the following tasks:
1. **Service Auditing**: The service is currently running somewhere on localhost. Find out which port it is listening on.
2. **CWE Identification**: Review `/home/user/app/server.go`. Identify the specific MITRE CWE identifier (format: "CWE-XXX") related to the insecure generation of its session tokens (cryptographic/randomness flaw).
3. **Audit Trail Generation**: Create a JSON file at `/home/user/audit_trail.json` with the following structure:
   ```json
   {
     "listening_port": <integer>,
     "vulnerability_cwe": "<string>",
     "remediation_action": "Applied CSP and Sandboxing"
   }
   ```
4. **Content Security Policy Enforcement**: Patch the `/home/user/app/server.go` file so that every HTTP response includes the following header exactly:
   `Content-Security-Policy: default-src 'self'; script-src 'none'; object-src 'none';`
5. **Process Isolation**: Create an executable bash script at `/home/user/sandbox.sh` that uses `bwrap` (Bubblewrap) to run the compiled `./server` binary from `/home/user/app/`. The script must enforce the following isolation:
   - A read-only bind mount of the host's root file system (`/` to `/`).
   - A read-write bind mount of the `/home/user/app` directory to itself.
   - Unshared network namespace (isolated networking).
   - Change directory to `/home/user/app` before executing `./server`.
   
Compile your patched Go server inside `/home/user/app/` as `server` (i.e., `go build -o server server.go`) and leave it there. Do not start the patched service yourself; the automated verification will run your `sandbox.sh` to test it.