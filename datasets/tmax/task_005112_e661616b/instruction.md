You are tasked with fixing and optimizing a resource analysis web service for a capacity planning team. 

There is a vendored Python application located at `/app/capacity-planner-1.0.0/`. It uses Flask and Gunicorn to serve resource analysis data. We also have an Nginx reverse proxy configuration file at `/app/nginx/capacity.conf`.

Currently, the setup is broken:
1. When Nginx and the Gunicorn service are running, making a request to `http://localhost:8080/analyze` returns a `502 Bad Gateway` error.
2. The `/analyze` endpoint in the Flask application is computationally expensive and slow.

Your objectives:
1. **Fix the 502 Error**: Identify and resolve the misconfiguration between Nginx and the Gunicorn upstream socket. Start both the Gunicorn application (as a daemon or background process) and Nginx using the provided config.
2. **Optimize Load Balancing / Caching**: The capacity planner tool will be hit heavily by automated CI/CD pipelines. Configure Nginx to proxy-cache responses from the `/analyze` endpoint for at least 10 seconds. You may modify `/app/nginx/capacity.conf` and Nginx's main configuration as needed. Nginx should run on port 8080.
3. **Task Automation Script**: Write a Python script at `/home/user/verify_capacity.py` that makes 50 concurrent requests to `http://localhost:8080/analyze`, asserts that all responses are `HTTP 200`, and exits with code 0 if successful.

To complete the task:
- Ensure both Nginx and the Gunicorn app are running in the background.
- Your Nginx cache configuration must ensure that subsequent requests to `/analyze` are served directly from the Nginx cache, dramatically reducing latency.
- The automated verification will run its own benchmark script against your Nginx port. To pass, the total time to serve 100 sequential requests to `/analyze` must be significantly lower than the baseline processing time of the Python app.