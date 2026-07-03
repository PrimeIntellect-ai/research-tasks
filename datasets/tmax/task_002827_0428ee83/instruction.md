You are a Release Manager preparing for a blue-green deployment of a new microservice. 
The legacy system currently uses a custom C++ caching component that has been failing to handle memory lifetimes correctly. We have decided to rewrite this specific component in Python and deploy it alongside the legacy mock for testing.

Your task consists of three phases:

**Phase 1: Code Translation & Custom Data Structure Design**
In `/home/user/legacy/cache.cpp`, there is a C++ implementation of a `PriorityLifoCache`. 
Read this file and translate the custom data structure into Python.
The data structure must strictly follow these rules based on the C++ logic:
- Items have a string `key`, a string `value`, and an integer `priority`.
- `put(key, value, priority)` adds or updates an item. If the key exists, its value and priority are updated, and it is marked as the most recently added among its priority level.
- `evict()` removes and returns the item with the *lowest* priority. If there are multiple items with the same lowest priority, it evicts the *most recently added or updated* item among them (LIFO order for ties).
- `get(key)` returns the value if it exists, or `None`.

Write this structure in `/home/user/green/server.py`. 

**Phase 2: Service Implementation**
In the same `/home/user/green/server.py` file, wrap your data structure in an HTTP server (you may use `Flask`, `FastAPI`, or Python's built-in `http.server`) listening on `127.0.0.1:8081`.
It must expose these endpoints:
- `POST /put` with JSON body: `{"key": "...", "value": "...", "priority": X}`. Returns HTTP 200.
- `POST /evict` returning JSON: `{"key": "...", "value": "..."}` or HTTP 404 if empty.
- `GET /get/<key>` returning JSON: `{"value": "..."}` or HTTP 404 if not found.

Start your Python server in the background.

**Phase 3: Reverse Proxy Configuration**
We need to route traffic between the legacy backend (which we will assume is running on `127.0.0.1:8080`) and your new green deployment on `127.0.0.1:8081`.
Create an Nginx configuration file at `/home/user/nginx.conf`.
The Nginx server must:
- Listen on `127.0.0.1:8000`.
- Run completely in user-space without root access (set `pid`, `error_log`, `access_log`, and all temp paths like `client_body_temp_path` to point inside `/home/user/nginx_data/`).
- Inspect the HTTP header `X-Deploy-Env`.
- If `X-Deploy-Env: green`, proxy the request to `127.0.0.1:8081`.
- Otherwise (if missing, or any other value), proxy the request to `127.0.0.1:8080`.

Create the `/home/user/nginx_data/` directory and start Nginx using your config.

To finish the task, write the string "DEPLOYMENT READY" to `/home/user/deployment.log`.