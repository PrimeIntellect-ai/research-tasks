You are a Site Reliability Engineer tasked with setting up a highly available backend service with automated rolling deployments and rollback capabilities. 

Your goal is to implement a simple HTTP server in C, configure an Nginx reverse proxy load balancer, and write a Bash script to handle safe rolling updates.

Complete the following phases:

**Phase 1: The C Backend**
1. Write a C program at `/home/user/server.c` that acts as a minimal HTTP server. 
2. It must accept a port number as its first command-line argument (`argv[1]`).
3. Whenever it receives a connection, it should immediately send the exact response: `HTTP/1.1 200 OK\r\n\r\nOK_V1\n` and close the connection.
4. Compile this program to `/home/user/server_bin`.
5. Start two instances of this server in the background, listening on ports `8081` and `8082`.

**Phase 2: Reverse Proxy & Load Balancer**
1. Create an Nginx configuration file at `/home/user/nginx.conf`.
2. The configuration must start an HTTP server listening on port `8080` that acts as a reverse proxy, load balancing requests round-robin between `127.0.0.1:8081` and `127.0.0.1:8082`.
3. Configure Nginx to run as a non-daemon and store its PID and temp files in `/home/user/nginx_tmp/` (create this directory) so it does not require root access.
4. Start Nginx in the background using this configuration.

**Phase 3: Rolling Deployment Script**
Write a Bash script at `/home/user/deploy.sh` that takes one argument: the path to a new C source file. The script must perform the following:
1. Create a backup directory at `/home/user/backup/` if it doesn't exist.
2. Copy the currently running `/home/user/server_bin` to `/home/user/backup/server_bin_$(date +%s)`.
3. Compile the provided new C source file, overwriting `/home/user/server_bin`.
4. Perform a staged deployment:
   a. Kill the process listening on port `8081`.
   b. Start the new `/home/user/server_bin` on port `8081`.
   c. Perform a health check by running a `curl` against `http://127.0.0.1:8081/`.
   d. If the health check fails (returns a non-0 exit code or does not connect), kill the failed process, restore the backup binary to `/home/user/server_bin`, start it on `8081`, and exit the script with an error.
   e. If the health check succeeds, repeat steps a-c for port `8082`.

**Phase 4: Execute an Update**
1. Copy `/home/user/server.c` to `/home/user/server_v2.c`.
2. Modify `/home/user/server_v2.c` so its response is `HTTP/1.1 200 OK\r\n\r\nOK_V2\n`.
3. Make `/home/user/deploy.sh` executable and run it using `/home/user/server_v2.c` as the argument to successfully deploy V2.
4. Once completed, query the load balancer (`curl -s http://127.0.0.1:8080`) and save the output to `/home/user/deploy_test.log`.

Ensure all background processes (the two C servers and Nginx) are running at the end of your interaction. Do not use sudo.