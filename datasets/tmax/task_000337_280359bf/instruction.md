You are tasked with securing and modernizing a legacy user account processing system for our site. We have a legacy stripped binary, `/app/legacy_auth_processor`, which processes user account creation and metadata update payloads. Unfortunately, it is vulnerable to directory traversal and command injection, but we cannot replace it right now.

Your objective is to:
1. **Filesystem Setup:** We have an image file at `/app/user_data.img`. Mount it at `/home/user/user_data_mnt` as a loop device (read-write) and ensure there is an `fstab` entry for it (you can place a local `fstab` snippet in `/home/user/local_fstab` since you don't have root).
2. **Sanitisation and Reverse Proxy:** Create a Python reverse proxy script at `/home/user/proxy.py` that listens on `127.0.0.1:8080`. This proxy must:
   - Accept incoming JSON HTTP POST requests to `/process`.
   - Implement a robust sanitiser that rejects any payload containing shell metacharacters, directory traversal sequences (like `../`), or suspiciously long strings (over 256 chars).
   - If the payload is malicious, return HTTP 403.
   - If the payload is clean, forward it to the legacy processor listening on `127.0.0.1:9090` and return its response.
3. **Service Management:** Write a bash script `/home/user/start_services.sh` that starts the legacy binary `/app/legacy_auth_processor` (it automatically binds to `9090`) and your Python reverse proxy in the background. Ensure the proxy implements a `/health` endpoint returning HTTP 200 `{"status": "ok"}`.
4. **Adversarial Validation:** There are two directories, `/app/corpus/clean/` and `/app/corpus/evil/`, containing test payload files. Your proxy's sanitiser logic must correctly accept 100% of the clean payloads and reject 100% of the evil payloads. You should test your logic locally against these files.

Please implement the proxy, the mount setup, and the startup script. Output a log file at `/home/user/setup_complete.log` with the string "READY" when you are done.