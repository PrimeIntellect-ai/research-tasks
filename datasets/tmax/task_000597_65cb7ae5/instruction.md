You are tasked with organizing and fixing the configuration for a multi-service web application that has been jumbled up. The application consists of Nginx, a Python Flask API, and a Redis server. The services have been started by a startup script, but they are misconfigured because the developer left the project files in a messy state.

All the messy files are located in `/app/messy_files`. 
Here is what you need to do:

1. **File Search & Bulk Rename:** 
   Find all configuration files in `/app/messy_files` that end with the `.prod.bak` extension. Rename all of them to remove the `.prod.bak` suffix and replace it with `.conf`.
   Similarly, find all Python files ending with `.py.bak` and rename them to end with `.py`.

2. **Text Transformation:**
   - In the newly renamed `.conf` files, use text transformation tools (like `sed` or `awk`) to replace all occurrences of the upstream address `backend.example.com:80` with `127.0.0.1:5000`.
   - In the newly renamed `.py` files, replace the string `DB_HOST = "redis.prod.internal"` with `DB_HOST = "127.0.0.1"`.
   - In the `.py` files, also replace `ENV = "production"` with `ENV = "development"`.

3. **Service Reconfiguration & Integration:**
   - Move the fixed Nginx configuration file (which should be named `nginx.conf`) to `/app/nginx/nginx.conf`, overwriting the existing broken one.
   - Reload or restart the Nginx server. It runs as a non-root user and is configured to listen on `127.0.0.1:8080`. You can test it using the provided Nginx binary: `/usr/sbin/nginx -c /app/nginx/nginx.conf -s reload` (or just kill and restart it).
   - Move the fixed Flask application file (which should be named `app.py`) to `/app/api/app.py`.
   - The Flask app is currently running but crashing. Find its process, kill it, and restart it in the background so it binds to `127.0.0.1:5000`. You can run it with `python3 /app/api/app.py &`.
   - Redis is already running correctly on `127.0.0.1:6379`.

Once everything is correctly placed and restarted, Nginx will proxy requests to the Flask API, which in turn will communicate with Redis. 

The automated verifier will make an HTTP GET request to `http://127.0.0.1:8080/health`. 
To succeed, the services must be running and the endpoint must successfully return the JSON response from the Flask app indicating that the environment is "development" and Redis is connected.