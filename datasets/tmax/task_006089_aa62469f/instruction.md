You are tasked with fixing a broken web application stack and automating part of its environment setup. 

We have a local Nginx reverse proxy configured to serve traffic over HTTPS and route it to a Python backend. However, the Nginx instance currently returns a "502 Bad Gateway" error because of a misconfiguration mimicking a network reachability issue, and the TLS certificates are missing.

Since you do not have root access, everything is isolated to the `/home/user/` directory.

Here is your objective:

1. **Idempotent Configuration Script**: 
   Write a Python script at `/home/user/idempotent_setup.py`. When executed, this script must idempotently perform the following tasks:
   - Parse the mock user database at `/home/user/mock_passwd`. If a user named `nginx_user` does not exist, append the exact line: `nginx_user:x:1005:1005:Nginx Dummy User:/home/user/nginx:/bin/false`. If it already exists, do not duplicate it.
   - Create the directory `/home/user/nginx/certs/` if it does not exist.
   - Generate a self-signed TLS certificate (`server.crt`) and private key (`server.key`) in `/home/user/nginx/certs/` using OpenSSL (e.g., via `subprocess`). The certificate should be 2048-bit RSA, valid for 365 days, and use `localhost` as the Common Name (CN). Do not overwrite them if valid files already exist.

2. **Fix the Reverse Proxy Misconfiguration**:
   - Inspect `/home/user/nginx/conf/nginx.conf`. The reverse proxy is failing to reach the backend service.
   - The backend service is provided at `/home/user/backend.py` and runs on `127.0.0.1:8000`.
   - Correct the routing misconfiguration inside `nginx.conf` so it points to the proper backend.

3. **Deploy and Verify**:
   - Run your `idempotent_setup.py` script.
   - Start the backend server in the background: `python3 /home/user/backend.py &`
   - Start the Nginx server in the background using its local config: `nginx -p /home/user/nginx -c /home/user/nginx/conf/nginx.conf &`
   - Verify the setup is working by making an HTTPS request to the Nginx proxy (which listens on port 8443 by default). Run `curl -k -s https://127.0.0.1:8443` and redirect the output exactly to `/home/user/proxy_test.log`.

Do not modify `/home/user/backend.py`. Ensure your `idempotent_setup.py` is written in Python and is strictly idempotent (running it 5 times should result in the exact same system state as running it once).