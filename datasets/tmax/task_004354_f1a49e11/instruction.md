You are a release manager preparing a deployment for a new REST API infrastructure. We have an architecture consisting of an Nginx reverse proxy, a new Python-based Sanitization API, and a Core Backend API. 

Currently, the deployment is broken in two ways:
1. The Nginx reverse proxy configuration (`/home/user/app/nginx.conf`) has a routing loop or misconfiguration. It should route all traffic arriving at `http://localhost:8080/api/` to the Sanitization service on port 8081.
2. The Sanitization service (`/home/user/app/sanitizer.py`) is incomplete. 

Your task is to fix the Nginx configuration and implement the Sanitization service in Python (using Flask or any standard library).

**System Architecture:**
- **Nginx Reverse Proxy:** Binds to `127.0.0.1:8080`. Should forward requests under `/api/` to the Sanitizer.
- **Sanitizer Service:** Binds to `127.0.0.1:8081`. 
- **Core Service:** Binds to `127.0.0.1:8082`. (Already implemented and running).

**Sanitizer Specification:**
The Sanitizer service must expose a `POST /api/patch` endpoint. It receives a JSON Patch payload (an array of operation objects as per RFC 6902, e.g., `[{"op": "replace", "path": "/name", "value": "Alice"}]`).
You must inspect the incoming JSON payload and ensure that no operation attempts to modify protected fields.
The protected root fields are `id`, `role`, and `is_admin`.
If *any* operation in the JSON array has a `path` that exactly matches `/id`, `/role`, or `/is_admin`, or falls under them (e.g., `/role/0`, `/is_admin/nested`), the Sanitizer MUST reject the request and return an HTTP `403 Forbidden` status code.
If the payload is safe (clean), the Sanitizer MUST forward the exact HTTP POST request (with the JSON body) to the Core Service at `http://127.0.0.1:8082/api/patch`. It should then return the exact HTTP status code and body it receives from the Core Service back to the client.

To run the stack, you can modify and execute `/home/user/app/start.sh`, which should launch Nginx, your Sanitizer, and the Core service in the background.

Ensure your sanitizer perfectly discriminates between valid profile updates and malicious privilege escalation attempts.