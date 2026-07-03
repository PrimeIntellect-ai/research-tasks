You are a System Administrator tasked with resolving a 502 Bad Gateway error on a local development environment and automating the deployment pipeline. 

Currently, there is an Nginx instance running as your unprivileged user. It is configured to listen on port 8080 and proxy requests to a local backend, but requests to `http://127.0.0.1:8080` are failing with a 502 error because the backend is not running on the expected port.

You have the following environment:
1. `/home/user/nginx/nginx.conf` - The Nginx configuration file currently in use. Nginx is already running.
2. `/home/user/backend.git` - A bare Git repository acting as the central deployment remote.
3. `/home/user/workspace` - A local clone of the backend repository containing a Python HTTP server (`app.py`). It has a remote named `origin` pointing to `/home/user/backend.git`.
4. `/home/user/deployed_app` - An empty directory where the deployed backend code should run.

Your objective is to fix the environment by performing the following steps:

1. **Create a Git Post-Receive Hook:**
   Write a `post-receive` hook inside `/home/user/backend.git/hooks/post-receive`. 
   The hook must:
   - Check out the latest code from the bare repository into `/home/user/deployed_app`.
   - Find and terminate any currently running instance of `app.py`.
   - Start the new `app.py` (using `python3`) in the background from `/home/user/deployed_app`.

2. **Fix the Application:**
   Analyze the Nginx configuration to find the upstream port it expects. Modify `/home/user/workspace/app.py` to listen on this correct port instead of its current port.

3. **Automate the Deployment with Python:**
   Write a Python script at `/home/user/auto_deploy.py`. When executed, this script must programmatically:
   - Stage the modified `app.py` in `/home/user/workspace`.
   - Commit the changes with the message "Fix backend port".
   - Push the changes to the `origin` remote to trigger the deployment hook.

4. **Verify:**
   Execute your `/home/user/auto_deploy.py` script. 
   Once the hook fires and the backend starts, test the proxy by running `curl -s http://127.0.0.1:8080`. 
   Save the exact standard output of this curl command to `/home/user/final_result.txt`.