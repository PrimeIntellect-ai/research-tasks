You are an administrator investigating a simulated Nginx 502 Bad Gateway error. The Nginx server is configured as a reverse proxy for a local Python backend application, but the backend is repeatedly failing to start and the Nginx configuration is pointing to the wrong port.

You need to perform a series of operations to fix the environment, correct the config, and write an automation script to reliably start the backend service.

Here are the requirements:

1. **Fix the Nginx Configuration & Backup:**
   The configuration file is located at `/home/user/nginx/nginx.conf`. It incorrectly points to port `8081` for the upstream backend, but the backend actually runs on port `8080`.
   Before you modify it, create a backup of this file at `/home/user/nginx/nginx.conf.bak`. Then, correct the proxy_pass port in the original file to `8080`.

2. **Storage Quota Management:**
   The backend logs data to `/home/user/backend/data.db`. Because of a strict internal storage quota check, the backend refuses to start if this file is over 1MB. Back up the file to `/home/user/backend/data.db.bak` and then truncate or delete the original `/home/user/backend/data.db` file so it is empty.

3. **Timezone Profile Setup:**
   The backend requires a specific timezone to parse its internal logs correctly. Create a shell profile file at `/home/user/.backend_env` that contains exactly the line: `export TZ="Europe/London"`.

4. **Interactive Backend Automation (Python):**
   The backend script at `/home/user/backend/server.py` expects to be run interactively. Upon startup, it prompts: `Enter start PIN:`. The correct PIN is `8573`.
   
   Write a Python script at `/home/user/run.py` that:
   - Uses the `pexpect` module (or standard library subprocess) to run the backend: `python3 /home/user/backend/server.py`
   - Injects the `TZ` environment variable (either by parsing/sourcing `/home/user/.backend_env` or directly passing the environment).
   - Automatically answers the `Enter start PIN:` prompt with `8573`.
   - Captures the final success output from the backend (which will say `Backend successfully started on port 8080`) and writes this exact output to a log file at `/home/user/resolution.log`.

Run your `run.py` script to generate the `resolution.log`. You do not need to leave the backend running as a daemon; it will cleanly exit after printing the success message once the correct PIN and environment are provided.