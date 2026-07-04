You are tasked with deploying a secure microservice environment and implementing a custom Web Application Firewall (WAF) classifier in Python. As a container specialist managing microservices, you must perform these tasks without `root` access. 

Your objectives are divided into three parts:

**Part 1: Architecture Configuration (Vision)**
We have received an architecture diagram snippet containing crucial deployment parameters. It is located at `/app/arch_config.png`.
You must extract the configuration values from this image. Specifically, you need to identify:
1. The upstream port for the microservice.
2. The directory where the pre-generated TLS certificates (`server.crt` and `server.key`) are located.

**Part 2: Custom WAF Classifier (Python)**
You must write a Python script at `/home/user/waf_classifier.py` that acts as a standalone request classifier.
The script must accept a single command-line argument (the path to a text file containing a raw HTTP request) and print exactly `ACCEPT` or `REJECT` to standard output.
You must analyze the incoming requests and reject any that contain:
- Path traversal attempts in the URI (e.g., `../` or `..%2f`).
- SQL injection keywords in the URI query string (e.g., `UNION SELECT`, `1=1`).
- Cross-Site Scripting (XSS) payloads in the body or headers (e.g., `<script>`, `javascript:`).
All other normal requests must be accepted. 
To ensure your script is robust, we have provided two testing directories:
- `/app/corpus/clean/`: Contains valid HTTP requests.
- `/app/corpus/evil/`: Contains malicious HTTP requests.
Your `waf_classifier.py` must correctly accept 100% of the clean requests and reject 100% of the evil requests.

**Part 3: Idempotent Deployment Script (Bash & Nginx)**
Write a bash script at `/home/user/deploy.sh` that performs an idempotent deployment of a user-space Nginx server.
The script must:
1. Generate an `nginx.conf` file in `/home/user/nginx.conf`.
2. Configure Nginx to listen on port `8443` (HTTPS) using the TLS certificates specified in the image.
3. Configure Nginx to proxy valid requests to the upstream port identified in the image.
4. Run Nginx as an unprivileged user using your custom config: `nginx -c /home/user/nginx.conf`. If Nginx is already running with this config, the script should reload it rather than failing.
5. Create any necessary directories for Nginx PID and logs within `/home/user/nginx_data/` to avoid permission errors.

Ensure your `deploy.sh` script is executable and handles errors gracefully. You do not need to integrate the `waf_classifier.py` directly into Nginx; the deployment of the Nginx server and the creation of the WAF classifier script are evaluated as separate components of this pipeline.