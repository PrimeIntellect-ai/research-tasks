You are a compliance analyst tasked with generating an audit trail for a recent security incident and patching the vulnerable service that caused it. 

We have an internal Single Sign-On (SSO) microservice vendored at `/app/vendored_sso_v1.2`. Security auditors have identified an open redirect vulnerability in the login flow. Attackers have been exploiting this by manipulating the `next` parameter to redirect users to malicious domains.

Your objectives are as follows:

1. **Fix the Vendored Service Setup**
   The service was vendored directly from a legacy repository, but its startup script (`/app/vendored_sso_v1.2/run.sh`) is currently broken due to a misconfigured environment variable for the binding port. Fix the script so that it correctly binds the service to port `8080`. 

2. **Patch the Open Redirect Vulnerability**
   The vulnerable code is in `/app/vendored_sso_v1.2/app.py`. The `/login` route takes a `next` query parameter to redirect users after a successful login. Currently, it accepts absolute URLs (e.g., `http://evil.com`). 
   Update `app.py` to ensure that the `next` parameter only accepts relative paths. Specifically:
   - It must start with a single forward slash `/`.
   - It must NOT start with double forward slashes `//` (to prevent protocol-relative redirects).
   - If the `next` parameter is missing, invalid, or violates these rules, default the redirect to exactly `/dashboard`.
   Do not add any external dependencies to the application.

3. **Generate the Audit Trail**
   You have been provided with historical HTTP access logs at `/home/user/historical_access.log`.
   Write a Python script to parse these logs and identify all successful (HTTP 200 or 302) requests to the `/login` endpoint where the `next` parameter contained an absolute URL (starting with `http://` or `https://`).
   
   Generate a JSON report at `/home/user/redirect_audit.json` formatted exactly like this:
   ```json
   [
     {
       "timestamp": "10/Oct/2023:13:55:36 -0700",
       "ip_address": "192.168.1.105",
       "malicious_target": "http://phishing-site.example.com/login"
     }
   ]
   ```
   Ensure the output is a valid JSON array.

4. **Deploy the Service**
   Once patched, run `/app/vendored_sso_v1.2/run.sh` so the service listens on `127.0.0.1:8080`. Leave it running in the background. Automated tests will send real HTTP requests to this port to verify your patch.