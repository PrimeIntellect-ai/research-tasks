You are a capacity planner building a local resource monitoring deployment. 

We have a custom C application that acts as an HTTP backend returning disk resource usage. It is designed to sit behind a user-space Nginx reverse proxy. However, our monitoring deployment is broken. When accessing the proxy, it returns a 502 Bad Gateway error because the C application is binding to the wrong UNIX domain socket path, and the proxy port isn't properly exposed to our internal metrics collector.

Your task is to fix the deployment and set up the automated collection script:

1. **Fix and Compile the C Application**:
   - The source code is located at `/home/user/app/disk_monitor.c`.
   - Update the code so the application binds to the correct socket expected by Nginx: `/home/user/app/backend.sock` (it is currently hardcoded to `wrong.sock`).
   - Compile the program to an executable named `/home/user/app/disk_monitor` and run it in the background.

2. **Start the Web Server**:
   - We have an Nginx configuration file ready at `/home/user/nginx/nginx.conf`.
   - Start Nginx in the background using this configuration and prefix: `nginx -c /home/user/nginx/nginx.conf -p /home/user/nginx`. 
   - Note: Nginx listens on port 8080.

3. **Configure Local Port Forwarding**:
   - Our metrics collector expects to connect on port 9090, but Nginx is on 8080.
   - Run a process in the background using standard CLI tools (like `socat` or `nc`) that listens on TCP port 9090 and forwards all traffic to TCP port 8080 on `127.0.0.1`.

4. **Automate the Monitoring**:
   - Write a bash script at `/home/user/check_capacity.sh`.
   - The script must perform an HTTP GET request to `http://127.0.0.1:9090/`.
   - Parse the response to extract the usage percentage (the app returns a string like `RESOURCE_USAGE: 42%`).
   - The script must append a line to `/home/user/capacity.log` in exactly this format:
     `[LOG] Usage is 42%` (replace 42% with whatever percentage the app actually returns).
   - Ensure the script is executable and execute it at least once so the log file is generated.