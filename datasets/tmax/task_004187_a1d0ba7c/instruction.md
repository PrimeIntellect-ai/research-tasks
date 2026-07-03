You are tasked with resolving a 502 Bad Gateway issue on our web server. 

We have a user-space Nginx instance configured via `/home/user/nginx.conf` that listens on port 8080. It is configured to reverse-proxy incoming requests to a Go backend service, but currently, any request to `http://127.0.0.1:8080/` results in a 502 Bad Gateway error.

The backend is a Go file server, the source for which is vendored at `/app/go-fileserver`. It is supposed to serve files from the `/home/user/data` directory on port 9000. However, the previous sysadmin made a botched edit to the Go source code, and it crashes on startup due to a hardcoded requirement for a non-existent mount point, and fails to handle incoming connections correctly.

Your objectives:
1. Identify and fix the bug in the vendored Go backend code at `/app/go-fileserver/main.go`. The server must run on port 9000 and serve files from `/home/user/data` without panicking.
2. Compile and start the Go backend as a background process.
3. Fix any misconfigurations in `/home/user/nginx.conf` so it correctly proxies traffic to the Go backend over port 9000.
4. Start Nginx using `nginx -c /home/user/nginx.conf`.
5. Ensure the setup is robust. We will run an automated load test against `http://127.0.0.1:8080/test.txt` when you are done. It must achieve a near-perfect success rate (no 502s) and high throughput.
6. Create an SSH tunnel config file at `/home/user/tunnel.sh` that contains the command to forward local port 8080 to a remote port 9999 on `localhost` (just write the command, no need to execute it).

Write a short log file `/home/user/fix.log` with a single line stating "Service Restored" when you are finished.