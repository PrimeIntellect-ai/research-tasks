You are tasked with fixing a deployment issue on a Linux server where Nginx is returning a 502 Bad Gateway error. 

System State:
- Nginx is running and configured to proxy requests from `http://127.0.0.1:8080` to a backend data service on `http://127.0.0.1:9000`.
- Currently, curling `http://127.0.0.1:8080/api/data` returns a 502 Bad Gateway.
- The backend service is provided as a vendored Python package located at `/app/data_service-1.2.0`. 
- The backend service is failing to start because of a bug in its storage monitoring logic (`disk_monitor.py`), which incorrectly calculates disk space requirements and immediately crashes the server.

Your objectives:
1. Diagnose and fix the perturbation in `/app/data_service-1.2.0/disk_monitor.py`. The script is supposed to ensure at least 500MB of free space in `/tmp`, but a logical error causes it to always fail.
2. The backend service MUST be started using the interactive legacy wrapper script located at `/app/data_service-1.2.0/bin/start_service.sh`. This script interactively prompts "Do you want to start the service? (y/n):". You must write a robust Expect script (or use Python's `pexpect` module) saved at `/home/user/start_backend.py` to automate answering this prompt and launch the service in the background.
3. Ensure the service stays running and Nginx successfully proxies requests to it, returning a 200 OK with the JSON payload `{"status": "ok", "data": "vendored_app_active"}`.
4. Write a robust Python script at `/home/user/verify_deployment.py` that handles network errors gracefully, sends 50 sequential requests to `http://127.0.0.1:8080/api/data`, and writes a file `/home/user/success_rate.txt` containing a single float (0.0 to 1.0) representing the ratio of 200 OK responses.

Do not modify the Nginx configuration. Nginx is already correctly configured to proxy to `127.0.0.1:9000`.