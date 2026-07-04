You are an engineer tasked with diagnosing a failing local deployment and standing up a local reverse proxy. 

A previous engineer left a backend service partially deployed. The service is launched via a shell script, but it immediately crashes when executed. It appears to be failing because it is trying to write logs and read configuration from the wrong location due to environment and path differences during execution.

Your task has four parts:

1. **Diagnose and Fix the Service:**
   The launcher script is located at `/home/user/launch.sh`. It starts a Python application located at `/home/user/app/app.py`. 
   Currently, executing `/home/user/launch.sh` fails. Fix `/home/user/launch.sh` so that it correctly sets the working directory to `/home/user/app/` before launching the app, and ensures the environment variable `DEPLOY_ENV` is set to `production`. Once fixed, run the script so the backend service starts on port 8081.

2. **Idempotent Configuration:**
   Write a Python script at `/home/user/configure.py`. This script must idempotently update the application's configuration file located at `/home/user/app/config.json`. 
   The script must ensure the JSON file contains the key `"proxy_active"` set to the boolean `true`, and `"backend_port"` set to `8081`. If the file does not exist, it should be created. If the file exists, these keys must be added or updated without removing any other existing keys in the JSON file. Run this script to update the configuration.

3. **Reverse Proxy:**
   Write a Python script at `/home/user/proxy.py` that acts as a simple reverse proxy. It must listen on `localhost` port `8000`. Any HTTP GET request made to `http://localhost:8000/` should be forwarded to `http://localhost:8081/`. The proxy should return the exact response body received from the backend service. Run this proxy script in the background.

4. **Verification:**
   Once the backend service and the reverse proxy are both running, execute a curl request to your proxy: `curl -s http://localhost:8000/` and redirect the output to `/home/user/proxy_test.log`.

Requirements:
- Do not modify `/home/user/app/app.py`.
- Use Python 3 for the scripts.
- The final state must have the backend running on 8081, the proxy running on 8000, and the correct response saved in `/home/user/proxy_test.log`.