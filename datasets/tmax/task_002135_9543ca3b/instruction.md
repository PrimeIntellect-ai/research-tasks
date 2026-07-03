Hello! Our staging environment is currently down. We have an Nginx reverse proxy configured to serve traffic on port 8080, routing to a Python backend API. However, any request to `http://127.0.0.1:8080/api/status` currently returns a 502 Bad Gateway.

The previous administrator left an architecture diagram image at `/app/system_layout.png`. This image contains a handwritten note with two critical pieces of information for the backend:
1. `API_SECRET`: A token the Python backend requires to start.
2. `SOCK_PATH`: The precise filesystem path where the backend should create its Unix domain socket.

Here is what you need to do:
1. **Extract Configuration**: Use `tesseract` (which is preinstalled) on `/app/system_layout.png` to read the `API_SECRET` and `SOCK_PATH`.
2. **Fix the Filesystem**: The Python backend expects to create its socket at the `SOCK_PATH`. You must create any necessary parent directories for this socket path inside `/home/user/backend/`. Ensure the directories have the correct permissions so the Python process can write to it and Nginx can read from it.
3. **Configure the Backend**: We have a Python backend script located at `/home/user/app/backend.py`. You need to run it in the background. It requires the environment variables `API_SECRET` and `SOCKET_PATH` (set to the values extracted from the image).
4. **Fix Nginx**: The Nginx configuration file is located at `/home/user/nginx/nginx.conf`. It is currently misconfigured to route traffic to `http://127.0.0.1:9000`. Modify `/home/user/nginx/nginx.conf` to proxy requests for `/api/` to the Unix domain socket path you extracted from the image. 
5. **Start Nginx**: Start Nginx using the corrected configuration file: `nginx -c /home/user/nginx/nginx.conf`.
6. **Verify**: You should be able to `curl -H "Authorization: Bearer <API_SECRET>" http://127.0.0.1:8080/api/status` and receive a 200 OK response with the JSON payload `{"status": "operational"}`.

Please implement these fixes. Leave both the backend and Nginx running in the background when you are finished.