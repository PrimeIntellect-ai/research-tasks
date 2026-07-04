You are a Cloud Architect migrating LegacyCorp's legacy infrastructure to a modern containerized environment. As part of this migration, you must fix a custom Python proxy, write a precise URL routing logic engine, and prepare configuration files for container deployment and storage mounting.

Complete the following tasks:

1. **Fix the Vendored Proxy Package:**
   There is a custom Python async reverse proxy package located at `/app/cloud-proxy-0.1.0`. It was partially developed but currently rejects all `POST` requests with a 403 status code due to a deliberate perturbation left by the previous developer.
   - Inspect the source code in `/app/cloud-proxy-0.1.0`.
   - Patch the logic so that `POST` requests are proxied normally instead of being rejected.
   - Install the package in editable mode (`pip install -e /app/cloud-proxy-0.1.0`).

2. **Implement the Routing Logic Engine:**
   Write a Python script at `/home/user/migrator_router.py` that computes the new backend destination for incoming HTTP request paths. The script must take exactly one positional argument (the incoming URI, including query parameters, e.g., `/api/v1/users?active=true`) and print exactly one line to standard output containing the mapped destination URL.
   
   Apply the following routing rules in order of precedence (first match wins):
   - **Rule A (Static):** If the URI starts with `/static/`, strip the `/static/` prefix and map it to a local file path: `/mnt/legacy_assets/<rest_of_path>`. (e.g., `/static/css/main.css` -> `/mnt/legacy_assets/css/main.css`)
   - **Rule B (PHP Legacy):** If the URI path (excluding query string) contains `.php`, map it to `http://lamp-legacy:80<original_path>`. However, you MUST sort any query parameters alphabetically by their keys in the output URL. (e.g., `/login.php?z=1&a=2` -> `http://lamp-legacy:80/login.php?a=2&z=1`)
   - **Rule C (API v1):** If the URI starts with `/api/v1/`, map it to `http://legacy-svc:8080<original_path>`.
   - **Rule D (API v2):** If the URI starts with `/api/v2/`, map it to `http://new-svc:9000<original_path>`.
   - **Default:** If none of the above match, map it to `http://default-router:8080<original_path>`.

3. **Storage & Container Configuration:**
   - Create a file at `/home/user/migration_fstab.txt` containing a single valid fstab entry to mount an NFS share `10.0.0.5:/var/nfs/legacy` to `/mnt/legacy_assets` using the `nfs4` filesystem type, with options `ro,nosuid,nodev,noexec,bg,soft,rsize=8192,wsize=8192`.
   - Create a docker-compose.yml file at `/home/user/docker-compose.yml` that defines a service named `cloud-proxy`. It should use the image `python:3.9-slim`, expose port 8080, and mount `/home/user/migrator_router.py` to `/usr/local/bin/router.py`.

Your URL router script will be aggressively tested against millions of random URL permutations to ensure 100% bit-exact parity with our reference implementation. Ensure edge cases like empty query strings or multiple question marks are handled cleanly.