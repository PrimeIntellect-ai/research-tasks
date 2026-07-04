You are an edge computing engineer deploying an application firewall to secure an IoT gateway. 

Our local gateway is running two services:
1. An Nginx reverse proxy, configured via `/home/user/gateway/nginx.conf` (running as the current user, listening on port 8080).
2. A Flask backend representing our IoT Telemetry API, listening on `127.0.0.1:5000`.

Currently, Nginx routes traffic on the `/telemetry` endpoint directly to the Flask backend. Recently, compromised edge devices have been sending malformed and malicious payloads.

Your task is to build and deploy a Python-based middleware WAF (Web Application Firewall) to filter out malicious telemetry, and reconfigure the gateway to use it.

Step 1: Write the Core Validator
Create a Python file at `/home/user/waf/validator.py`. It must contain a function with the following exact signature:
`def is_clean(payload_str: str) -> bool:`
This function must parse a JSON string and return `True` if it is clean, and `False` if it is malicious or malformed.
A payload is considered "clean" if and only if:
- It is a valid JSON object.
- It contains exactly two top-level keys: `"device_id"` and `"readings"`.
- The `"device_id"` is a string containing exclusively alphanumeric characters and hyphens (no spaces, no SQL/shell injection characters).
- The `"readings"` key is a JSON object where every value is strictly a number (integer or float). 

Step 2: Create the Middleware Proxy
In the same directory, create `/home/user/waf/proxy.py`. This must be a lightweight Python HTTP server listening on `127.0.0.1:8081`. 
- When it receives a `POST` request on `/telemetry`, it should read the body and pass it to `is_clean()`.
- If clean, it must forward the exact request body to the Flask API (`http://127.0.0.1:5000/telemetry`), wait for the response, and return that response to the client with a `200 OK`.
- If malicious, it must immediately return a `403 Forbidden` response without forwarding the payload to Flask.

Step 3: Gateway Configuration
Modify `/home/user/gateway/nginx.conf` so that requests to `/telemetry` are routed to your new Python proxy on port `8081` instead of directly to port `5000`. Once modified, reload or restart the Nginx process.

Step 4: Deployment Hook
We track our WAF configuration in a local Git repository located at `/home/user/waf`.
Initialize this directory as a Git repository, add your Python scripts, and create a Git hook (`post-commit`) that automatically restarts the `proxy.py` script in the background whenever a new commit is made. Make an initial commit to ensure your hook executes and the proxy is running.

Ensure everything is running. The automated tests will send telemetry through Nginx on port 8080 to verify your end-to-end traffic flow and will run a large suite of malicious and clean payloads directly against your `validator.py`.