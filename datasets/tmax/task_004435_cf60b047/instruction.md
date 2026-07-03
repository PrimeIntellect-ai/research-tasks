You are a deployment engineer tasked with rolling out an update for a local load balancer that routes traffic to our backend application servers. You need to configure the environment, set up the reverse proxy, and write a connectivity diagnostic script to verify the deployment.

Perform the following tasks:

1. **Environment Setup:**
   Modify `/home/user/.bashrc` to permanently export the following environment variables:
   - `APP_LB_PORT=8080`
   - `APP_B1_PORT=9001`
   - `APP_B2_PORT=9002`

2. **Reverse Proxy Configuration:**
   Create an HAProxy configuration file at `/home/user/haproxy.cfg`. 
   The configuration must:
   - Run in the foreground or as a daemon (but do not use privileged `user` or `group` directives since you do not have root access).
   - Have a `frontend` named `app_front` that binds to `127.0.0.1` on the port defined by `APP_LB_PORT` (use the literal port number `8080` in the file).
   - Route traffic to a `backend` named `app_back` using the `roundrobin` algorithm.
   - The backend must define two servers, `backend1` and `backend2`, pointing to `127.0.0.1` on ports `9001` and `9002` respectively.
   - Use `mode http` for both frontend and backend.

3. **Diagnostic Script:**
   Create a Bash script at `/home/user/verify.sh`. 
   - The script must be executable (`chmod +x`).
   - It should perform an HTTP GET request to `http://127.0.0.1:8080/health` exactly 4 times using `curl` (use the `-s` flag to suppress the progress meter).
   - Wait 1 second between each request.
   - Append the exact raw output of each `curl` command to a log file located at `/home/user/health_check.log`, with each response on a new line.

Do not start HAProxy or the backend servers yourself; our automated testing framework will source your `.bashrc`, launch the mock backends, start HAProxy with your configuration, and then execute your `verify.sh` script to validate the deployment.