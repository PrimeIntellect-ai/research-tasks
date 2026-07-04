You are a build engineer managing release artifacts. A recent storage issue corrupted several build packages. You have a JSON manifest of the artifacts that contains their expected custom parity checksums, which you must use to identify the safe artifacts. 

Your objective is to write a Bash script that parses this manifest, mathematically verifies the integrity of each file, and automatically generates and runs an Nginx reverse proxy configuration. This proxy will serve the healthy artifacts and block the corrupted ones.

Here are the specific requirements:

1. **Working Directory & Artifacts:**
   All operations should occur in `/home/user/workspace`. 
   Assume there are four tarballs in `/home/user/workspace/artifacts`: `build_alpha.tar`, `build_beta.tar`, `build_gamma.tar`, and `build_delta.tar`.
   The manifest file is located at `/home/user/workspace/artifacts/manifest.json`.

2. **Parity Verification Logic:**
   You must write a Bash script `/home/user/workspace/verify_and_route.sh` that parses the `manifest.json`.
   For each artifact, calculate the mathematical parity `P` as follows:
   - Compute the sum of the decimal ASCII values of all characters in the exact filename (e.g., "A.bin" -> 65 + 46 + 98 + 105 + 110 = 424).
   - Get the file size in bytes.
   - Calculate `P = (file_size XOR ascii_sum) MOD 251`. (XOR is the bitwise exclusive OR operation).
   
   If `P` matches the `expected_parity` in the JSON manifest, the file is valid. If it does not match, the file is corrupted.

3. **Backend Server:**
   Start a simple Python HTTP server on port `9000` serving the directory `/home/user/workspace/artifacts/`. Leave it running in the background.

4. **Reverse Proxy Configuration:**
   Your Bash script must dynamically generate an Nginx configuration file at `/home/user/workspace/nginx.conf` based on the verification results. 
   - Nginx must listen on port `8080`.
   - For requests to `/download/<filename>`:
     - If the artifact is **valid**, Nginx must act as a reverse proxy and pass the request to the Python backend (`http://127.0.0.1:9000/<filename>`).
     - If the artifact is **corrupted** (invalid parity), Nginx must return an HTTP `403 Forbidden` status code.
   
   *Nginx Non-Root Skeleton:*
   To help you avoid permission issues when running Nginx without root privileges, ensure your generated `nginx.conf` structure includes the following directives at the top level/HTTP block:
   ```nginx
   pid /home/user/workspace/nginx.pid;
   events { worker_connections 1024; }
   http {
       access_log off;
       error_log /home/user/workspace/nginx_error.log;
       client_body_temp_path /tmp/client_body;
       proxy_temp_path /tmp/proxy_temp;
       fastcgi_temp_path /tmp/fastcgi_temp;
       uwsgi_temp_path /tmp/uwsgi_temp;
       scgi_temp_path /tmp/scgi_temp;
       server {
           listen 8080;
           # Your dynamically generated location blocks here
       }
   }
   ```

5. **Execution:**
   Once the script generates the configuration, use it to start Nginx in the background:
   `nginx -c /home/user/workspace/nginx.conf`

Ensure both the Python backend and the Nginx proxy are running and properly configured to route or block requests before you declare the task finished.