You are tasked with migrating a legacy Web Application Firewall (WAF) service from Python 2 to Python 3, fixing its integration with a Go-based reverse proxy, and improving its detection logic against a new set of malicious payloads.

Your workspace is located in `/app/`.

Here is the current architecture:
1. **Frontend Proxy (`/app/proxy/`)**: A Go reverse proxy that listens on port `8000`. It receives incoming JSON requests, forwards them to the WAF for inspection, and if approved, forwards them to the backend. It uses goroutines to handle concurrent requests.
2. **WAF Service (`/app/waf/`)**: A legacy Python 2 HTTP server (`waf.py`) listening on port `5000`. It receives payloads from the proxy, deserializes them (handling base64 and hex encodings), and checks for malicious patterns. 
3. **Backend (`/app/backend/`)**: A simple Python 3 API listening on port `9000` that processes valid requests.

Your objectives:
1. **Python 3 Migration**: Port `/app/waf/waf.py` to Python 3. Resolve all `bytes` vs `str` discrepancies that arise during base64 decoding and JSON deserialization, and update the HTTP server library from `BaseHTTPServer` to `http.server`.
2. **Multi-Service Composition**: Ensure the end-to-end flow works. The Go proxy must successfully communicate with the Python 3 WAF and the Backend. You will need to start all three services in the background. 
3. **Adversarial Defense**: The current WAF logic is failing to catch modern attacks while dropping legitimate traffic. We have provided two corpora of payloads:
   - `/app/corpus/clean/`: Contains strictly benign JSON payloads.
   - `/app/corpus/evil/`: Contains malicious JSON payloads (e.g., nested SQLi, XSS, and deserialization exploits).
   Update the sanitization logic in `waf.py` so that it correctly rejects 100% of the evil payloads (returning an HTTP 403 status code) and accepts 100% of the clean payloads (returning an HTTP 200 status code).
4. **Classification Report**: Write a Python script at `/home/user/classify.py` that imports your updated WAF logic, iterates through all files in `/app/corpus/clean/` and `/app/corpus/evil/`, and writes the classification results to `/home/user/classification.json`. 

The format of `/home/user/classification.json` must be a flat JSON object where keys are the base filenames (e.g., `payload_01.json`) and values are either the string `"clean"` or `"evil"`.

Once you have finished, ensure all three services (proxy, WAF, backend) are running in the background and `/home/user/classification.json` is generated.