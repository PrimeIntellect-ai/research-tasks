You are an infrastructure engineer automating the provisioning and deployment of a custom internal web service.

We have a broken deployment located in `/home/user/app/`. The system consists of an Nginx reverse proxy and a Go backend. Currently, sending an HTTP request to Nginx results in a 502 Bad Gateway error because the proxy is pointing to a non-existent or incorrectly configured upstream Unix socket. 

Your goal is to fix the application code, correct the configurations, implement a missing monitoring endpoint, and write a deployment script.

Here are your specific requirements:

1. **Fix the Nginx Configuration**: Inspect `/home/user/app/nginx.conf`. It is configured to listen on `127.0.0.1:8080`. Note the upstream Unix socket path it expects. Correct the file if the path seems misconfigured, or adjust the backend to match. Nginx is already running using this configuration file.

2. **Fix the Go Backend**: 
   - Modify `/home/user/app/main.go` so that the HTTP server listens on the exact Unix domain socket expected by Nginx (e.g., `/home/user/app/backend.sock`). 
   - Ensure that whenever the Go server starts, it cleans up any pre-existing socket file at that path and sets the appropriate permissions (ACLs) so that Nginx (running as the `user` user) can read and write to the socket.

3. **Implement Storage Monitoring**:
   - Update the `/status` route in `main.go`. It must dynamically calculate the total disk space used by regular files within the `/home/user/app/data/` directory (recursively).
   - The endpoint must return an HTTP 200 status code with a JSON response in this exact format:
     `{"data_bytes": <TOTAL_BYTES>}`
     (where `<TOTAL_BYTES>` is the integer sum of the sizes of all regular files in that directory).

4. **Construct a CI/CD Deployment Script**:
   - Create an executable bash script at `/home/user/app/deploy.sh`.
   - The script must automate the deployment by:
     a) Building the Go application, saving the binary to `/home/user/app/server`.
     b) Terminating any currently running instances of `/home/user/app/server`.
     c) Starting the newly built Go backend in the background.
     d) Reloading the Nginx configuration gracefully (using `nginx -s reload -c /home/user/app/nginx.conf`).

You must run `./deploy.sh` to apply your changes. Once Nginx and your Go backend are successfully communicating, the automated test will verify the system.