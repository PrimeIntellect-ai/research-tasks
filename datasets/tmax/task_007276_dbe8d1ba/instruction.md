You are a capacity planner analyzing the resource usage of several QEMU virtual machines. A colleague has set up a local resource reporting API written in Go, which runs behind a local Nginx reverse proxy. 

However, the setup is currently broken. If you were to start the services, requesting the Nginx endpoint would result in a 502 Bad Gateway error due to a misconfiguration in the upstream socket path.

Your task is to fix the setup, get the services running, and generate a capacity report.

Here are the details of the environment:
- The Go API source code is located at `/home/user/app/api.go`. When executed, it listens on a UNIX socket for HTTP requests.
- The local Nginx configuration file is located at `/home/user/nginx/nginx.conf`. It is configured to run entirely in user-space without root privileges, listening on port `8080`.

Perform the following steps:
1. Identify and fix the typo in `/home/user/nginx/nginx.conf` that causes the 502 Bad Gateway error (the proxy path does not match the socket path used by the Go application).
2. Start the Go API in the background.
3. Start Nginx in the background using the corrected configuration. Use the command: `nginx -c /home/user/nginx/nginx.conf -p /home/user/nginx`
4. Write a bash script at `/home/user/check_capacity.sh` that uses `curl` to send a GET request to `http://127.0.0.1:8080/stats` and saves the exact HTTP response body to a file named `/home/user/capacity_report.txt`.
5. Execute the bash script to generate the `/home/user/capacity_report.txt` file.

Ensure that by the end of your execution, `/home/user/capacity_report.txt` exists and contains the correct JSON payload from the Go API. Do not use `su` or `sudo`.