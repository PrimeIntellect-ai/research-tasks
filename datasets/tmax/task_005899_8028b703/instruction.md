You are a system administrator tasked with fixing a broken web service. We have an Nginx reverse proxy running entirely in user-space, which is supposed to proxy requests to a custom backend HTTP service written in C++. 

Currently, when we make a request to the Nginx endpoint, we receive a "502 Bad Gateway" error. You must diagnose and fix the entire pipeline, from the Nginx configuration down to the C++ source code.

Here is the current state of the system:
- Nginx prefix directory: `/home/user/nginx/`
- Nginx config file: `/home/user/nginx/nginx.conf`
- Nginx is listening on port `8080`.
- The backend source code is located at `/home/user/backend/server.cpp`.

Your tasks:

1. **Backup Strategy**: Before making any modifications, back up the Nginx configuration file. Copy `/home/user/nginx/nginx.conf` to `/home/user/backup/nginx.conf.bak`. Create the backup directory if it does not exist.

2. **Fix and Compile the C++ Backend**: 
   - Inspect `/home/user/backend/server.cpp`. There are two issues: it is hardcoded to listen on the wrong port (it currently binds to `8000`, but our architecture requires the backend to run on port `9000`), and it might have other minor logical bugs preventing it from returning the correct HTTP response. 
   - Modify `server.cpp` so that it listens on `127.0.0.1:9000` and successfully responds to incoming HTTP GET requests with `HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nBackend OK!\n`.
   - Compile the backend using `g++ /home/user/backend/server.cpp -o /home/user/backend/server`.

3. **Expect Scripting**: 
   - The C++ backend is designed to require an interactive security PIN upon startup. When executed, it prints `Enter PIN: ` to stdout and waits for stdin. The correct PIN is `7788`.
   - Write an Expect script at `/home/user/backend/start.exp` that automates launching `/home/user/backend/server`, waits for the `Enter PIN: ` prompt, submits `7788`, and then hands over control or keeps the process running in the background so it can serve requests.
   - Run your Expect script so the backend is actively listening.

4. **System Config Management**: 
   - Fix the Nginx configuration file (`/home/user/nginx/nginx.conf`). It is currently proxying the `/api` location to the wrong upstream port (which causes the 502 Bad Gateway). Update it to point to the correct backend port (`9000`).
   - Start Nginx in the background using the command: `nginx -p /home/user/nginx -c /home/user/nginx/nginx.conf`

5. **Verification**: 
   - Once everything is running, test the pipeline by making an HTTP request to Nginx: `curl -s http://localhost:8080/api`
   - Save the exact text output of this `curl` command into a log file at `/home/user/result.log`. The automated test will check the contents of `/home/user/result.log` and the existence of your backup.