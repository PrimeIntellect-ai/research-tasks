You are an operations engineer responsible for a local deployment pipeline. We have a staging environment set up on this machine, but the deployment is currently failing. 

When a developer pushes code to the bare Git repository at `/home/user/staging.git`, a `post-receive` Git hook is triggered. This hook attempts to deploy the Python web application and an Nginx reverse proxy. However, the deployment script reports that the service is failing its health check (returning a 502 Bad Gateway), and the backend Python application process appears to be crashing immediately on startup.

Your objectives are to diagnose and fix the deployment pipeline so that pushing to the staging repository results in a healthy, running service.

Here are the specific components and their locations:
1. **Git Repositories**: 
   - Bare staging repository: `/home/user/staging.git`
   - Developer workspace: `/home/user/workspace` (cloned from `staging.git`)
2. **Nginx Configuration**: `/home/user/config/nginx.conf` (configured to run entirely in user-space, listening on port 8080).
3. **Application**: A Python WSGI app using Gunicorn, located in the repository. The application binds to a UNIX socket.
4. **Deployment Script**: The `post-receive` hook is located at `/home/user/staging.git/hooks/post-receive`. It copies the latest code to `/home/user/deploy_target`, starts the services, and runs a health check against `http://127.0.0.1:8080/health`.

You must identify and resolve the following issues:
1. **Routing Bug**: The Nginx configuration is returning a 502 because it is pointing to the wrong upstream UNIX socket path. Inspect the application startup command in the hook and correct the Nginx configuration.
2. **Environment Bug**: The Python application enforces strict locale and timezone requirements on startup. It expects the timezone (`TZ`) to be set to `UTC` and the locale (`LANG`) to be set to `en_US.UTF-8`. Update the deployment script/hook so that the Python process receives the correct environment variables.
3. **Trigger Deployment**: Once you have fixed the configurations and the hook, you must commit your changes in `/home/user/workspace` and run `git push origin master`. 

**Success Criteria:**
- The `git push` command completes successfully (exit code 0) and the deployment hook reports a successful health check.
- Nginx is running and successfully proxying requests.
- Running `curl -s http://127.0.0.1:8080/health` returns exactly `{"status": "ok"}`.
- Do not use root/sudo. Ensure all fixes are made using the `/home/user` paths provided.