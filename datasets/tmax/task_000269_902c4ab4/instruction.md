You are an infrastructure engineer for a red-team operation. Your team uses a local "C2 Relay" architecture to communicate with a compromised target backend. We need to upgrade this relay to prevent junior operators from sending noisy injection payloads that would burn our access, securely encrypt the traffic, and redact sensitive liability data (PII) before it reaches our central logging server.

We have a multi-service setup located in `/app/`:
1. **Nginx** (`/app/nginx/nginx.conf`): Listens on TCP port 8443. It is currently broken because the TLS certificates are missing.
2. **Target Backend emulator** (`/app/backend/server.py`): A simple Flask API listening on TCP 5000. It returns operational data.

Your tasks:

**Phase 1: TLS and Hashing**
1. Generate a self-signed TLS certificate (`cert.pem`) and private key (`key.pem`) in `/app/certs/`. Nginx is pre-configured to look for them there.
2. Nginx must forward traffic to a new intermediary C2 Relay Proxy you will write, which must listen on TCP port 8080. Nginx is already configured to proxy requests to `http://127.0.0.1:8080`.

**Phase 2: The C2 Relay Proxy (WAF & Redaction)**
Write a proxy service (in Python, Node.js, or your preferred language) that listens on `127.0.0.1:8080` and forwards requests to the target backend at `127.0.0.1:5000`. 
Your proxy must enforce the following rules:
1. **Payload Filtering (Adversarial Corpus)**: Junior operators often send bad XSS or basic SQLi payloads. Your proxy must inspect the `q` URL parameter of incoming GET requests.
   - If the payload contains basic noisy signatures (e.g., `<script>`, `OR 1=1`, `UNION SELECT`), it must immediately return an HTTP 403 status code.
   - If the payload is clean, it must forward the request to the backend.
   - To build your filter, you have been provided with two directories of sample payload files: `/app/corpus/evil/` (noisy payloads that MUST be blocked) and `/app/corpus/clean/` (stealthy or benign payloads that MUST be forwarded). Your proxy must achieve 100% accuracy on these sets.
2. **Data Redaction**: The backend sometimes returns target credit card numbers in the JSON response (e.g., `{"status": "ok", "data": "User 123 paid with 4532-1111-2222-3333"}`). Your proxy must intercept the response from the backend and redact any 16-digit credit card number (formatted as `XXXX-XXXX-XXXX-XXXX`) by replacing it with `[REDACTED]`.
3. **Cryptographic Checksum**: To authenticate our tooling, the proxy must only process requests if they include an `X-Auth-Hash` header containing the SHA256 hash of the string `redteam_operation_2024`. If this header is missing or incorrect, return an HTTP 401.

**Phase 3: Integration**
Ensure all services can be started. You should write a script `/home/user/run_all.sh` that:
1. Starts the Flask backend in the background.
2. Starts your C2 Relay Proxy in the background.
3. Starts Nginx (e.g., `nginx -c /app/nginx/nginx.conf -g "daemon off;"`) in the background.

The automated test will invoke `/home/user/run_all.sh`, wait 3 seconds, and then fire requests directly to `https://127.0.0.1:8443/api?q=<payload>` using the corpora to verify your end-to-end flow, TLS configuration, header authentication, filtering, and redaction.