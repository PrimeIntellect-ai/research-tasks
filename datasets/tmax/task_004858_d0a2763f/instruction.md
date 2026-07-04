You are a system administrator tasked with fixing a broken web service and securing it. 

We have a local web application stack in `/home/user/app_stack/`. It consists of an Nginx reverse proxy and a Python backend. When properly configured, the Nginx server should listen on port `8080` and proxy requests to the backend. Currently, if you start the Nginx server and curl it, you get a "502 Bad Gateway" error because the proxy configuration is pointing to the wrong port, and the backend isn't running.

Furthermore, the application is currently completely open, but we need to secure it using HTTP Basic Authentication, managed via a custom bash script.

Your objectives are:

1. **Fix the Proxy configuration:** 
   Analyze `/home/user/app_stack/nginx/nginx.conf` and the backend script at `/home/user/app_stack/backend/server.py`. Find the port mismatch and fix `nginx.conf` so it correctly points to the backend's actual listening port.

2. **Implement User Management (Bash Scripting):**
   Write a Bash script at `/home/user/app_stack/manage_auth.sh` that acts as an account administration tool. 
   - The script must accept two positional arguments: a username and a plaintext password (e.g., `./manage_auth.sh <user> <pass>`).
   - It must generate an Apache-compatible htpasswd entry (using `openssl passwd` or similar) and append it to `/home/user/app_stack/nginx/.htpasswd`.
   - Ensure the script is executable.
   - Use your script to create a user with the username `sysadmin` and the password `supersecurepass`.

3. **Secure Nginx:**
   Modify `/home/user/app_stack/nginx/nginx.conf` to enforce HTTP Basic Authentication for the root location `/`. 
   - Use the authentication realm `"Restricted Area"`.
   - Point the user file to the `.htpasswd` file you generate.

4. **Start Services and Verify (Connectivity Diagnostics):**
   - Start the backend server in the background.
   - Start Nginx as an unprivileged user using the command: `nginx -c /home/user/app_stack/nginx/nginx.conf -p /home/user/app_stack/nginx/`
   - Write a connectivity diagnostic script at `/home/user/app_stack/test_connection.sh`. This bash script should use `curl` to make an authenticated request to `http://127.0.0.1:8080/` as the `sysadmin` user. 
   - The script must write its output to `/home/user/app_stack/final_result.log` in the exact following format on a single line:
     `HTTP_STATUS: <status_code>, BODY: <response_body>`
     (For example: `HTTP_STATUS: 200, BODY: Hello World`)

Ensure all services are running and the `final_result.log` file is successfully generated with the correct 200 status code and backend response before completing the task.