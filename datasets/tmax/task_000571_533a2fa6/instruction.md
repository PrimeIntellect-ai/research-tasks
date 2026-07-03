You are an operations engineer troubleshooting a failed local deployment. A user-space Nginx reverse proxy is supposed to serve a Python backend web application, but requests to the proxy currently return a "502 Bad Gateway" error.

Your goals are to automate the backend deployment process, diagnose the connectivity issue, fix the Nginx configuration, and verify the fix.

Here is the environment setup:
- There is an interactive deployment script at `/home/user/deploy.sh` that starts the Python backend. It prompts the user for two inputs:
  1. `Environment (dev/prod):`
  2. `Confirm start? [y/N]:`
- The Nginx configuration file is located at `/home/user/nginx/nginx.conf`. 
- Nginx is configured to listen on port `8080`.

Perform the following steps:

1. **Automate the Deployment**: The backend must be started by interacting with `/home/user/deploy.sh`. Write an `expect` script named `/home/user/auto_deploy.exp` that automates this interaction. It should provide `prod` for the environment and `y` for the confirmation. Run your expect script to start the backend.
2. **Diagnose and Fix Nginx**: Determine why Nginx is returning a 502 error. You will need to inspect the running Python backend (check which port it actually bound to) and compare it to the Nginx upstream configuration in `/home/user/nginx/nginx.conf`. Fix the Nginx configuration so it correctly routes to the Python backend.
3. **Start/Reload Nginx**: Start Nginx in the background using the corrected configuration: 
   `nginx -p /home/user/nginx -c /home/user/nginx/nginx.conf`
   (If it is already running, you may need to reload or kill and restart it).
4. **Verify**: Once the proxy is correctly routing traffic to the backend, run a `curl` command against the Nginx server (`http://127.0.0.1:8080/`) and save the raw HTTP response body to `/home/user/resolution.log`.

Do not modify the backend Python code or the `deploy.sh` script. Only configure the `expect` script and the Nginx configuration.