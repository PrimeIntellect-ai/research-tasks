You are tasked with building a lightweight Bash-based Web Application Firewall (WAF) and orchestrating a multi-service backend environment. 

You have been provided with a codebase in `/home/user/app/` containing a microservice architecture:
- An Nginx load balancer (config at `/home/user/app/nginx/nginx.conf`)
- A Python Flask service (`/home/user/app/flask/`)
- A Go-based authentication service (`/home/user/app/go-auth/`)
- A Redis instance (already installed on the system)

Your objectives are as follows:

1. **Build and Compose Services:**
   - The Go authentication service needs to be compiled. You must cross-compile it for both `linux/amd64` and `linux/arm64` architectures. Place the resulting binaries in `/home/user/app/go-auth/build/` named `auth-amd64` and `auth-arm64`.
   - Write a startup script at `/home/user/start_services.sh` that:
     a) Starts a local Redis server on port 6379.
     b) Starts the Flask application (which runs on port 8081).
     c) Starts the compiled Go authentication service (`auth-amd64`) on port 8082.
     d) Starts Nginx using the configuration file at `/home/user/app/nginx/nginx.conf` (Nginx should listen on port 8080).
   - *Ensure Nginx routes `/api/` to the Flask service and `/auth/` to the Go service. You will need to edit `nginx.conf` to configure these reverse proxies.*

2. **Adversarial WAF Detector:**
   - We need to filter incoming requests before they hit the backend. You must write a Bash script at `/home/user/detector.sh`.
   - The script will take a single argument: the file path to a raw HTTP request dump.
   - `detector.sh` must parse the HTTP request and exit with status `0` (clean) or `1` (malicious/evil) based on the following rules:
     - **Semantic Versioning:** The request must contain an `X-API-Version` header. If the header is missing, or if the semantic version is strictly less than `1.5.0` (e.g., `1.4.9`, `0.9.0`), the request is evil.
     - **Path Traversal:** If the HTTP Request-URI contains `../` or the URL-encoded equivalent `%2e%2e%2f` (case-insensitive), the request is evil.
     - Otherwise, the request is clean.
   - You can test your script against the corpora provided in `/home/user/corpus/clean/` and `/home/user/corpus/evil/`. Your script must perfectly classify both directories.

3. **Integration:**
   - Start all your services using `/home/user/start_services.sh`. Ensure Nginx, Redis, Flask, and the Go service are running concurrently and that Nginx correctly proxies the traffic.

Ensure your `detector.sh` is robust, executable (`chmod +x`), and strictly uses Bash. Do not use Python, Perl, or Ruby for the detector script.