You are acting as a system administrator and developer. We have a local continuous deployment (CD) pipeline failing because our web server returns a "502 Bad Gateway" error. 

Our application architecture consists of a C++ HTTP backend application that communicates over a Unix Domain Socket, sitting behind an Nginx reverse proxy. Both run in userspace. 

Currently, the setup is failing. The Nginx configuration expects the backend to listen on `/home/user/run/upstream.sock`, but the C++ backend code has a misconfigured socket path.

Your tasks are:

1. **Fix the C++ Backend**: Modify the C++ source file located at `/home/user/app/server.cpp` to bind to the correct Unix socket path (`/home/user/run/upstream.sock`). Make sure the directory `/home/user/run/` exists before the application binds to it.

2. **Create a Deployment Pipeline Script**: Write a robust, executable Bash script at `/home/user/deploy.sh` that automates the build, service lifecycle, and verification. The script must:
    - Use "set -e" to fail on errors.
    - Compile the C++ application using `g++ /home/user/app/server.cpp -o /home/user/app/server_bin`.
    - Ensure any old sockets at `/home/user/run/upstream.sock` are removed before starting the server.
    - Start the compiled C++ backend (`/home/user/app/server_bin`) in the background.
    - Start the local Nginx instance using: `nginx -p /home/user/nginx -c /home/user/nginx/nginx.conf`
    - Wait a few seconds to ensure services are fully up.
    - Perform an HTTP GET request to Nginx at `http://127.0.0.1:8080/` and save *only* the HTTP response body to `/home/user/test_result.log`.
    - Use a `trap` to gracefully terminate both the C++ backend and the Nginx server when the script exits (or upon failure). The `deploy.sh` script should exit successfully (0) after completing these steps.

Do not use `sudo` or modify system-wide configurations; everything must run within the `/home/user` workspace using unprivileged ports. Do not output the direct commands to me; perform the fixes and create the script.