You are a container specialist managing a local microservice environment. We have an Nginx reverse proxy meant to route requests to a backend microservice written in C. However, the service is currently failing with a 502 Bad Gateway error when accessing `http://127.0.0.1:8080/api` because the upstream socket path is mismatched and permissions are not strictly controlled.

Your environment contains the following files:
1. `/home/user/app/server.c`: The source code for the backend C application. It listens on a Unix domain socket and speaks basic HTTP.
2. `/home/user/nginx/nginx.conf`: The Nginx configuration file configured to run in user-space.

Your task is to fix the application and configure the system correctly. 

Follow these requirements:
1. **Fix the C Code**: Modify `/home/user/app/server.c` so that the Unix socket path it binds to is exactly `/home/user/run/app.sock`.
2. **Fix Nginx Configuration**: Modify `/home/user/nginx/nginx.conf` so that the `proxy_pass` directive for the `/api` location points correctly to the Unix socket at `/home/user/run/app.sock`.
3. **Idempotent Automation Script**: Create a bash script at `/home/user/setup.sh` that performs the following steps in an idempotent manner (it should run successfully even if run multiple times):
    - Create the directory `/home/user/run` and set its permissions strictly to `700` (so only the owner can access the socket).
    - Compile the `/home/user/app/server.c` file using `gcc`, outputting the binary to `/home/user/app/server`.
    - Stop any previously running instances of the C backend server and Nginx (gracefully handle if they are not running).
    - Ensure any old socket file at `/home/user/run/app.sock` is removed before starting the backend.
    - Start the compiled C server backend in the background.
    - Start Nginx in the background using the provided configuration: `nginx -c /home/user/nginx/nginx.conf -p /home/user/nginx` (Ensure Nginx stays running; you may need to adjust daemon settings or run it in the background if it is set to daemon off).
    - Sleep for 1 second to allow services to initialize.
    - Run a `curl` command against `http://127.0.0.1:8080/api` and save ONLY the response body to `/home/user/success.log`.

Make sure `/home/user/setup.sh` is executable (`chmod +x /home/user/setup.sh`).

The final verification will check:
- `server.c` and `nginx.conf` have the correct socket paths.
- The `/home/user/run` directory has the correct `700` permissions.
- The `setup.sh` script works completely.
- `/home/user/success.log` contains exactly the text `Hello Microservice`.