You are acting as a security auditor for a newly acquired e-commerce startup. Your task is to investigate and secure their internal API architecture, which is currently suffering from authorization bypass and injection vulnerabilities. 

The environment relies on a multi-service architecture located in `/app/ecommerce_stack/`:
1. An Nginx reverse proxy routing traffic on port 8080.
2. A Flask Python backend running on port 5000 that processes orders and user metadata.
3. A Redis cache running on port 6379 for session management.

There are two main objectives you must complete:

**Objective 1: Multi-Service Configuration Fix**
The system is misconfigured, allowing unauthenticated internal routing bypasses. Specifically, the Nginx configuration and the Flask backend's permission validation are mismatched. Nginx forwards requests to Flask, but HTTP header inspection reveals that internal administrative headers (`X-Internal-Role`) can be spoofed by external users if they manipulate their cookies or craft specific HTTP headers. 
You must analyze the startup scripts, Nginx configs (`/app/ecommerce_stack/nginx/nginx.conf`), and Flask application logic (`/app/ecommerce_stack/backend/app.py`). Reconfigure Nginx and Flask so that Nginx aggressively strips any `X-Internal-Role` headers from incoming external traffic, while ensuring the end-to-end flow of a legitimate internal service request (which we will simulate via a local proxy test) still works.

**Objective 2: WAF Filter Creation**
The Flask application is vulnerable to malicious payloads embedded in HTTP headers and cookies. In `/home/user/waf_filter.py`, write a Python script that acts as an automated vulnerability detector and sanitiser. 
Your script must implement a function with the exact signature: `def verify_request(headers: dict, cookies: dict) -> bool`. 
It should return `True` if the request is clean and should be allowed, and `False` if it contains malicious payloads (e.g., directory traversal, SQLi fragments, or forged admin cookies).

To assist you, the previous auditors left a corpus of serialized request data (JSON files containing headers and cookies dictionaries). 
- Legitimate traffic examples are in `/app/corpus/clean/`.
- Known malicious payloads are in `/app/corpus/evil/`.

Your `waf_filter.py` will be tested against these corpora. It must correctly reject 100% of the evil corpus and preserve 100% of the clean corpus.

Complete your fixes in the `/app/ecommerce_stack/` directory and save your Python filter to `/home/user/waf_filter.py`. Once completed, write a log file at `/home/user/audit_complete.log` containing the text "AUDIT FINISHED".