I am building a small C-based utility backend, but I am running into build issues and I need you to set up a reverse proxy in front of it.

I have a C project in `/home/user/backend`. When I run `make`, it fails due to a circular dependency in the `Makefile`. 

Here is what you need to do:
1. **Fix the Makefile:** Investigate `/home/user/backend/Makefile` and resolve the circular dependency so that `make` successfully compiles the `server` executable.
2. **Start the backend:** Run the compiled `server` executable in the background. It will automatically listen on `127.0.0.1:8080`.
3. **Configure Nginx:** I have provided a base Nginx configuration file at `/home/user/nginx.conf` which is configured to run as a non-root user. You need to edit this file to add a `server` block listening on port `8000` with the following requirements:
   - Route all requests for `/api/` to the C backend at `http://127.0.0.1:8080/`.
   - Validate incoming requests to `/api/`: Requests must contain an HTTP header `X-Utility-Key` with the exact value `secret123`. If the header is missing or incorrect, Nginx should return a `403 Forbidden` status immediately without forwarding the request.
   - Enforce rate limiting on the `/api/` route: Limit requests to 1 request per second per client IP (`$binary_remote_addr`). Ensure burst requests are rejected immediately (return `503 Service Unavailable` for excess requests).
4. **Start Nginx:** Run Nginx in the background using your modified config: `nginx -c /home/user/nginx.conf`.
5. **Log completion:** Once everything is running, create an empty file at `/home/user/success.log` to indicate you are finished.

Do not use `sudo`; everything must run as the default `user`.