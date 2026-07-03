You are acting as a backup operator validating the restore procedure for our custom analytics service. The automated restore script has unpacked the service into `/home/user/restore`, but the service is currently broken. When both Nginx and the backend are started, Nginx returns a 502 Bad Gateway error because it cannot communicate with the upstream backend daemon.

Your task is to fix the configuration, update the backend code, and successfully start the service:

1. Examine the Nginx configuration located at `/home/user/restore/nginx.conf`. It is configured to listen on `127.0.0.1:8080` and proxy requests to a Unix domain socket.
2. Examine the C source code for the backend daemon at `/home/user/restore/src/backend.c`. There is a mismatch between the socket path Nginx expects and the socket path the backend binds to. 
3. Fix the Nginx configuration and/or the C code so that both use the exact same socket path: `/home/user/restore/run/backend.sock`.
4. Modify `/home/user/restore/src/backend.c` so that upon startup, the daemon writes its Process ID (PID) to `/home/user/restore/run/backend.pid`.
5. Compile the fixed C code using `gcc` and output the executable to `/home/user/restore/bin/backend`.
6. Start the compiled backend process in the background.
7. Start Nginx locally using the command: `nginx -c /home/user/restore/nginx.conf -p /home/user/restore/`
8. Verify the service is working by running `curl -s http://127.0.0.1:8080/api`. Save the exact output of this curl command to `/home/user/restore/success.txt`.

Ensure all processes are running and the `success.txt` file contains the correct HTTP response body from the C daemon.