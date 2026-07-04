You are a system administrator taking over a staged deployment of a new internal data processing service. 

Currently, the deployment is failing. When users send a POST request to the local Nginx endpoint at `http://127.0.0.1:8080/api/process`, they receive a "502 Bad Gateway" error. 

The system consists of:
1. An Nginx reverse proxy running locally. Its configuration file is located at `/home/user/deployment/nginx/nginx.conf`.
2. A Python backend service (Gunicorn + Flask) running in the background. It is supposed to serve requests on a local socket or port, but the Nginx configuration is completely misaligned with the backend's actual binding.
3. A missing core processing engine. The Flask application shells out to a Python script located at `/home/user/deployment/processor.py` to process the data, but this script is currently empty.

Your objectives:
1. **Fix the Nginx Configuration:** Investigate the Nginx configuration and the backend service to figure out why the 502 Bad Gateway error is occurring. Reconfigure Nginx so that it correctly routes traffic to the Python backend. Nginx must run on port 8080.
2. **Implement the Processor:** Write the Python script at `/home/user/deployment/processor.py`. This script must read a line of text from standard input (stdin) and print the processed output to standard output (stdout).
   - We have provided a compiled oracle binary of the expected processor logic at `/app/oracle_processor`.
   - Your Python script's behavior must be bit-for-bit identical to the oracle binary for any arbitrary input string. You can test your script against the oracle to deduce the string transformation logic (it involves a specific character substitution and run-length encoding mechanism).
   - Make sure your script has the correct permissions to be executed by the backend.

Constraints:
- You must write your solution in Python 3.
- Do not modify the Flask backend code itself, only the Nginx configuration and the `processor.py` script.
- Ensure Nginx is restarted/reloaded to apply your fixes. You can run Nginx in the foreground or background using the provided configuration directory.