You are acting as a FinOps analyst responsible for optimizing cloud costs and managing the internal Cost Dashboard. 

Your environment has a multi-service architecture running locally. A startup script at `/app/start.sh` launches a Gunicorn/Flask API and a local Nginx instance. 
Currently, the dashboard is broken, and we need to implement a strict admission controller for cloud deployment requests.

Complete the following tasks:

1. **Fix the Multi-Service Compose (Dashboard)**
   - Start the services using `/app/start.sh`.
   - Nginx is listening on port 8080, but `curl http://localhost:8080/health` returns a 502 Bad Gateway.
   - The Nginx configuration is located at `/home/user/nginx.conf`. It is currently pointing to the wrong upstream UNIX socket (`/tmp/wrong_dashboard.sock`).
   - The Flask app actually binds to `/tmp/cost_dashboard.sock`. Update the Nginx configuration to point to the correct socket and reload Nginx so that the health check returns a 200 OK.

2. **Web Server "Firewall" Rule**
   - We are receiving unauthorized scraping requests from `198.51.100.55`. Add a directive to `/home/user/nginx.conf` to explicitly deny all requests from this IP address at the server block level.

3. **Environment Locale & Timezone Wrapper**
   - The cost calculations require strict timezone and locale settings.
   - Create a shell script at `/home/user/run_filter.sh` that sets the environment variables `TZ="Etc/UTC"` and `LC_ALL="en_US.UTF-8"`, and then executes the Python admission controller (created in step 4) passing all arguments to it.

4. **Write the Admission Controller (Adversarial Corpus)**
   - We must prevent expensive infrastructure from being deployed.
   - Write a Python script at `/home/user/cost_filter.py` that takes a single command-line argument: the path to a JSON file representing a deployment request.
   - The script must read the JSON file. It should exit with status code `0` (Allow) ONLY IF it passes our cost rules. It must exit with status code `1` (Reject) if it violates any rule.
   - **Rules for Rejection (Evil):**
     - The JSON contains a `resources` list. If any item in that list has `"type": "compute"` AND its `"size"` starts with the letter `"x"` or `"p"` (e.g., "x1.large", "p3.8xlarge").
     - If any item in the `resources` list has a `"monthly_cost"` strictly greater than `500`.
   - We have provided a set of test files to validate your script. Your script must successfully exit `0` for all files in `/app/corpus/clean/` and exit `1` for all files in `/app/corpus/evil/`.

Ensure all files are created exactly at the specified paths.