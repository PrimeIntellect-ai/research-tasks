I am trying to run a local, rootless web stack with Nginx acting as a reverse proxy for a custom backend service written in C. However, `curl http://localhost:8080` is currently returning a "502 Bad Gateway" error. 

The system is supposed to use a staged deployment directory structure (similar to Capistrano) so that we can easily roll back, but the deployment structure is missing and the backend code has bugs. 

I need you to fix the backend C code, write an idempotent deployment script to set up the directory structure, and get the service running correctly behind Nginx.

Here is what you need to do:

1. **Fix the C Backend (`/home/user/src/backend.c`)**:
   I have started writing a simple HTTP backend in C at `/home/user/src/backend.c` that listens on a UNIX socket. Currently, it crashes or fails to start. 
   - Fix the code so it successfully binds to a UNIX socket. The path to the socket must be passed as the first command-line argument (`argv[1]`).
   - The backend must accept incoming connections and respond to any HTTP request with the exact following plaintext HTTP response:
     ```
     HTTP/1.1 200 OK
     Content-Length: 18
     Connection: close

     SUCCESS_DEPLOYMENT
     ```
   - Ensure the backend properly unlinks the socket file before binding if it already exists, to prevent "Address already in use" errors.

2. **Write the Deployment Script (`/home/user/deploy.sh`)**:
   Write a bash script that performs a staged deployment. The script must be completely idempotent (it should succeed whether it's run the first time or the tenth time).
   - It should create a base directory at `/home/user/app/`.
   - Inside `/home/user/app/`, manage a `releases/` directory.
   - Every time the script runs, it should generate a new release directory based on the current UNIX timestamp (e.g., `/home/user/app/releases/<timestamp>`).
   - Compile `/home/user/src/backend.c` and place the executable inside this new release directory, naming it `backend_service`.
   - Update a symlink at `/home/user/app/current` to point to the new release directory.
   - Gracefully kill any existing `backend_service` processes.
   - Start the new `backend_service` in the background, passing `/home/user/app/current/backend.sock` as the socket path argument.

3. **Start the Infrastructure**:
   - Run your `deploy.sh` script to perform the initial deployment.
   - Start Nginx in the background using the configuration file I already placed at `/home/user/nginx.conf` (Run: `nginx -c /home/user/nginx.conf`).
   
When you are done, an automated test will run `curl -s http://localhost:8080/` which must output exactly `SUCCESS_DEPLOYMENT`. The test will also check the existence and structure of `/home/user/app/current` and `/home/user/deploy.sh`.