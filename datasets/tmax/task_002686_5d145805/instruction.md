You are acting as an incident responder for a company that recently suffered a breach. The attackers exploited a vulnerability in our internal binary analysis service.

The service architecture consists of:
- An Nginx reverse proxy listening on port 8080.
- A Flask application running on port 5000 that processes ELF binaries uploaded by users.
- A Redis instance on port 6379 managing authentication tokens.

We have gathered a dataset of requests containing ELF payloads. Some of these contain malicious exploit payloads (encoded shellcode, malformed headers designed to buffer overflow the parser), while others are legitimate binaries our developers uploaded.

Your tasks are to:
1. Write a Python script `/home/user/waf.py` that acts as a middleware or standalone filter. It should read a directory of raw HTTP requests (each saved as a file) and classify them.
2. The script must be invoked as: `python3 /home/user/waf.py --input-dir <dir> --output-file /home/user/results.json`. The output must be a JSON dictionary mapping the filename to a boolean (`true` if malicious/reject, `false` if clean/accept).
3. Reconfigure the Nginx service (config located at `/etc/nginx/sites-available/default`) to route incoming uploads to your WAF script (or a service running your script) before passing them to the Flask application, effectively blocking malicious payloads. Since you don't have root, Nginx is configured to run as `user` and its config is in `/home/user/nginx/nginx.conf`. (Actually, wire up the services using the provided startup script `/home/user/start_services.sh`).

The malicious payloads exhibit specific anomalies in their ELF headers or contain known encoded reverse shell payloads in the `.data` section. Your script must parse the ELF structure from the HTTP body to detect these anomalies.

Ensure your `waf.py` accurately flags the malicious payloads without blocking the clean ones. Write your script to be robust against various encodings used in the malicious corpus.