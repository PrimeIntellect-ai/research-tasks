You are tasked with securing a new polyglot build system's web gateway. The system accepts configuration expressions and source code patches via a JSON API, but it currently lacks input validation and is exposed to malicious payloads.

Your goal is to build a Web Application Firewall (WAF) in Python, configure a reverse proxy, and ensure only safe payloads reach the backend build service.

**System Architecture:**
1. **Backend Build Service:** Runs locally on `127.0.0.1:8081`. It accepts POST requests to `/build` with a JSON payload: `{"expression": "<math/logic string>", "patch": "<unified diff string>"}`. (This service is already running).
2. **WAF Service:** You must create a Flask application at `/home/user/waf.py` that listens on `127.0.0.1:8080`.
3. **Reverse Proxy:** You must configure a local Nginx instance to listen on `127.0.0.1:8000` and proxy all traffic to your WAF service on port 8080.

**Your Tasks:**

1. **Configure Nginx (Reverse Proxy):**
   Create or modify the Nginx configuration at `/home/user/nginx.conf` so that Nginx listens on `127.0.0.1:8000` and proxies all requests to `http://127.0.0.1:8080`. You should start Nginx using this configuration file (`nginx -c /home/user/nginx.conf`).

2. **Implement the Python WAF (`/home/user/waf.py`):**
   Write a Flask application listening on `127.0.0.1:8080`. It must intercept POST requests. It should read the JSON payload containing `expression` and `patch`.
   
   *Filter Rule 1 (Expression Evaluation Protection):* The `expression` string must only contain safe Python abstract syntax tree (AST) nodes. Specifically, it must only allow basic math, string literals, and basic variable names. If it contains function calls (e.g., `__import__`, `eval`), attribute access, or any execution-oriented AST nodes, you must reject the request.
   
   *Filter Rule 2 (Patch Directory Traversal Protection):* The `patch` string contains a unified diff. You must parse the diff and ensure that any file paths specified in the `---` or `+++` lines do NOT contain absolute paths (starting with `/`) and do NOT contain directory traversal sequences (`../`).

   *Action:* 
   - If the payload violates *either* rule, the WAF must return an HTTP 403 Forbidden response.
   - If the payload is completely safe, the WAF must forward the exact JSON payload to the backend build service at `http://127.0.0.1:8081`, and return the backend's HTTP response code and body back to the client.

**Testing Your Setup:**
There are two corpora of payloads provided for you to test against:
- `/app/corpus/clean/`: Contains JSON files with safe expressions and valid patches.
- `/app/corpus/evil/`: Contains JSON files with malicious expressions (e.g., RCE attempts) or malicious patches (e.g., modifying `/etc/passwd`).

Your WAF must allow 100% of the clean corpus to pass through (returning 200 OK from the backend) and block 100% of the evil corpus (returning 403 Forbidden directly from the WAF).