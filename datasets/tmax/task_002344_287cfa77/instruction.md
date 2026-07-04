You are a container specialist tasked with fixing a broken microservice deployment and creating a monitoring utility.

Currently, we have a backend service running locally on port 5000, and a user-space Nginx instance configured via `/home/user/nginx.conf`. There are two main issues you must resolve:

**1. Service Composition and TLS Configuration**
The Nginx server is supposed to act as a secure reverse proxy on port 8443, but it's currently failing. 
- You need to generate a self-signed TLS certificate (`/home/user/cert.pem`) and private key (`/home/user/key.pem`) valid for `localhost`.
- Edit `/home/user/nginx.conf` to enable SSL/TLS on port 8443 using these certificates.
- Add a routing rule in the Nginx configuration so that any request to `/health` is forwarded (proxied) to the backend service at `http://127.0.0.1:5000`.
- Once configured, ensure Nginx is running and picks up the new configuration (you can run `nginx -c /home/user/nginx.conf` or reload it if already running).

**2. Monitoring Metrics Parser**
Our health-check system generates raw metric strings that need to be parsed into a strict JSON format for our monitoring daemon.
Create an executable script at `/home/user/parse_metrics` (in any language you prefer, such as Python, Bash+jq, etc.). 
- The script must read a single line from `stdin`.
- The input will be a comma-separated list of key-value pairs separated by a colon, e.g., `cpu:45,status:UP,mem:1024`.
- The script must output a single line of minified JSON representing these metrics under a `data` object.
- **Rules:**
  - Strip any leading/trailing whitespace from keys and values.
  - All extracted values must be represented as strings in the JSON, even if they are numeric.
  - The keys inside the `data` object **must be sorted alphabetically**.
  - Example Input: ` mem: 512, cpu: 80, status: RUNNING `
  - Example Output: `{"data":{"cpu":"80","mem":"512","status":"RUNNING"}}`

Ensure both the Nginx proxy successfully serves the backend's `/health` endpoint over HTTPS and the `parse_metrics` script perfectly adheres to the specified parsing rules.