You are an observability engineer building a local deployment pipeline for some custom dashboard configurations. 

Please perform the following steps to set up the pipeline:

1. Create a local bare Git repository at `/home/user/dashboards.git`.
2. Generate a self-signed TLS certificate and private key at `/home/user/cert.pem` and `/home/user/key.pem` respectively (valid for localhost, no password).
3. Create a shell script `/home/user/deploy_env.sh` that exports a single environment variable `DEPLOY_ENV=prod`.
4. Create a Git `post-receive` hook at `/home/user/dashboards.git/hooks/post-receive`. The hook must:
   - Read the standard input (which Git provides as `oldrev newrev refname`).
   - Source the `/home/user/deploy_env.sh` file.
   - Check if `DEPLOY_ENV` is exactly `prod`.
   - If it is `prod`, run a Python script `/home/user/deploy.py` (which you must also create) and pass the `newrev` as the first command-line argument.
5. Write the Python script `/home/user/deploy.py` so that it takes the Git commit hash (the `newrev`) and extracts the contents of that commit from `/home/user/dashboards.git` into the directory `/home/user/www/dashboards/`. (Create this directory if it doesn't exist. You can use `git archive` via `subprocess` or any other method to extract the files).
6. Create a Python script `/home/user/server.py` that runs an HTTPS web server serving the directory `/home/user/www/` on port `8443`. It must use the certificate and key you generated (`/home/user/cert.pem` and `/home/user/key.pem`). 
7. Start the server script `/home/user/server.py` in the background and save its process ID to `/home/user/server.pid`.

Ensure all file paths are exact, the Git hook is executable, and the web server uses TLS successfully.