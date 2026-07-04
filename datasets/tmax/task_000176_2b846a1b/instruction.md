You are a FinOps analyst responsible for maintaining a lightweight, localized cloud cost reporting dashboard. To avoid expensive SaaS tools, your team deployed a custom Python backend (Flask) managed by `supervisord` and served via `nginx` running entirely in user-space.

Currently, the deployment is broken and incomplete. You need to fix the deployment, implement a deployment automation script via Git hooks, and verify the system is working.

Here are the system details and your objectives:

1. **Fix the 502 Bad Gateway Error:**
   - Nginx is running as the user and listening on port `8080`. Its configuration is located at `/home/user/nginx/nginx.conf`.
   - Supervisor is managing the Python application. Its configuration is at `/home/user/supervisor/supervisord.conf`.
   - Currently, making a request to `http://localhost:8080/api/costs` returns a 502 Bad Gateway. The Nginx config is expecting an upstream UNIX socket at `/home/user/run/app.sock`, but the application is binding to a different address.
   - Fix the configuration (either Nginx or Supervisor) so they communicate correctly over the UNIX socket (`/home/user/run/app.sock`), and restart the necessary services using their respective configurations. Nginx command: `nginx -p /home/user/nginx -c /home/user/nginx/nginx.conf -s reload`. Supervisor command: `supervisorctl -c /home/user/supervisor/supervisord.conf update` and `restart`.

2. **Automate Data Deployments (Git Hook):**
   - Cost data updates are pushed to a local bare Git repository located at `/home/user/cost-data.git`.
   - The application serves data from a JSON file located via a symlink at `/home/user/app_data/current/cost.json`.
   - Write a `post-receive` Git hook in **Python** at `/home/user/cost-data.git/hooks/post-receive`. Ensure it is executable.
   - The hook must do the following on every push:
     a. Read the `<oldrev> <newrev> <refname>` from standard input.
     b. Extract the contents of `<newrev>` into a new directory: `/home/user/app_data/releases/<newrev>` (using `git archive` or similar).
     c. Validate that `cost.json` exists in the newly extracted directory. If it does not, print an error and exit with a non-zero status.
     d. Safely update the symlink `/home/user/app_data/current` to point to the new directory `/home/user/app_data/releases/<newrev>`.
     e. Restart the application process using `supervisorctl -c /home/user/supervisor/supervisord.conf restart finops_app`.

3. **Verify the Deployment:**
   - Clone the repository `/home/user/cost-data.git` to `/home/user/workspace`.
   - Create a file named `cost.json` in the repository containing: `{"status": "optimized", "total": 150.50}`
   - Commit and push the changes to the `main` branch.
   - Wait 2 seconds, then make a `curl` request to `http://localhost:8080/api/costs`.
   - Save the HTTP response body to `/home/user/verification.log`.

Note: You do not have root access. All paths must be absolute as provided above.