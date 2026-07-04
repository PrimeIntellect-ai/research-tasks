You are an incident responder investigating a recent breach on a company's infrastructure. The attacker exploited an open redirect vulnerability in the login flow and bypassed our reverse proxy restrictions.

Your objective consists of two parts:

**Part 1: Service Reconfiguration (Multi-service Compose)**
Our application stack located in `/app/` consists of an Nginx reverse proxy and a Flask authentication service.
The services are started via `/app/start.sh`. Currently, the end-to-end flow is broken.
You must modify `/app/nginx.conf` so that:
1. Nginx listens on port `8080`.
2. All requests to `/` are proxied to the Flask application running on `127.0.0.1:5000`.
3. The `Host` header is preserved and passed to the upstream Flask app.
4. Access to the `/admin` path via Nginx must return a 403 Forbidden.

Ensure that after your modifications, running `/app/start.sh` successfully brings up Nginx and Flask, and `curl http://127.0.0.1:8080/login` correctly routes to the Flask app.

**Part 2: Open Redirect Detection (Adversarial Corpus)**
The attacker left behind extensive logs. We need a reliable way to filter out malicious redirect attempts from clean traffic.
Write a Bash script at `/home/user/url_filter.sh` that takes a single file path as its argument. The input file will contain a list of redirect target URLs (one per line). 
Your script must print to `stdout` ONLY the URLs that are safe, omitting any open redirect payloads. 

A safe URL in our context is:
- A relative path (e.g., `/dashboard`, `/profile?user=1`)
- An absolute URL pointing strictly to our domain: `https://myapp.local` (e.g., `https://myapp.local/settings`)

A malicious URL (open redirect attempt) includes:
- Absolute URLs pointing to other domains (e.g., `http://evil.com/login`, `https://myapp.local.evil.com/`)
- Protocol-relative URLs (e.g., `//malicious.site/`)
- `javascript:` or `data:` URIs

Your script will be evaluated against a test corpus of clean and evil URLs. It must correctly preserve all clean URLs and reject all evil URLs. Ensure the script is executable.