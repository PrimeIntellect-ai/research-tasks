You are managing a microservice architecture and need to build a new Python-based reporting service that analyzes a surveillance video and securely serves the results. 

Here are your tasks:

1. **Video Analysis:**
   A video file is located at `/app/surveillance.mp4`. Using `ffmpeg` and Python, analyze this video and determine the exact total number of frames it contains.

2. **Secure Token Retrieval (SSH Tunneling):**
   The authorization token needed to secure your new service is provided by an internal microservice running on port 8000 of an isolated container. You can only access this container via SSH on `localhost:2222`. 
   However, the local SSH configuration (`~/.ssh/config`) for the host alias `auth-service` has been misconfigured and is silently rejecting key-based login. 
   - Fix the SSH configuration so you can authenticate using your default key.
   - Establish a local port forwarding tunnel (map local port 8000 to remote port 8000).
   - Once the tunnel is up, fetch the secret token by making a GET request to `http://localhost:8000/token`. The response will be plain text.

3. **Service Deployment:**
   Write and start a Python HTTP service (using the standard library or Flask) located at `/home/user/server.py`. 
   - The service must read the `API_PORT` environment variable and listen on that port on all interfaces (`0.0.0.0`). Set `API_PORT=8080` in your shell profile (`~/.bashrc`) and ensure the service uses it.
   - Expose an endpoint `GET /stats`.
   - The endpoint must require an `Authorization: Bearer <token>` header, using the exact token you retrieved from the internal microservice.
   - If the token is correct, return an HTTP 200 response with the following JSON payload: `{"total_frames": N}` (where N is the integer frame count you extracted).
   - If the token is missing or incorrect, return an HTTP 401 response.
   - Start the service in the background so it remains running.

Ensure your service is up and running on port 8080 and correctly validates the token before returning the frame count.