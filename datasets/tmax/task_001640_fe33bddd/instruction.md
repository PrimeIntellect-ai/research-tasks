You are a developer tasked with organizing a broken mathematical project. The project consists of multiple modules that must be evaluated in a specific dependency order. 

Currently, the dependency metadata for these modules is stored in text files. You need to build a system that dynamically calculates the correct build execution order using a topological sort, exposes this via a REST API, and serves it behind an Nginx reverse proxy.

Here are the precise requirements:

1. **Dependency Graph Parsing:**
   There is a directory at `/home/user/math_nodes/` containing several `.txt` files. The name of the file (excluding `.txt`) is the name of the module (e.g., `A.txt` represents module `A`).
   Each file contains exactly one line: a comma-separated list of modules that this module depends on. If a file is empty, the module has no dependencies.
   
2. **REST API Construction:**
   Write a web server (using any language/framework of your choice) that runs on `127.0.0.1:8080`. 
   It must have a `GET /build_order` endpoint.
   When requested, this endpoint must:
   - Read the `/home/user/math_nodes/` directory.
   - Parse the dependencies.
   - Perform a topological sort to determine the build order (modules with no dependencies must be built first).
   - **Tie-breaking rule:** If multiple modules are ready to be built (i.e., they have 0 unmet dependencies), you must process them in **alphabetical order**. Use a standard Kahn's algorithm where the queue of ready nodes is kept sorted alphabetically.
   - Return a JSON array of strings representing the evaluated build order. Example: `["Module1", "Module2"]`. Ensure the `Content-Type` is `application/json`.

3. **Reverse Proxy Configuration:**
   Configure an Nginx reverse proxy to expose this API.
   - Create an Nginx configuration file at `/home/user/nginx.conf`.
   - The Nginx server must listen on `127.0.0.1:9000`.
   - It must proxy requests from `GET /api/v1/build_order` to `http://127.0.0.1:8080/build_order`.
   - Since you do not have root access, configure your `nginx.conf` to use `/home/user/` for its `pid`, `error_log`, and `access_log` files, and run it as the current user. 
   - Start the Nginx process in the background. Ensure both your API server and Nginx are running at the end of the task.

Start by examining the files in `/home/user/math_nodes/` (you will need to wait for the environment to initialize them, or you can assume they exist when your scripts run), write your API server, write the Nginx config, and start the services. Ensure `curl -s http://127.0.0.1:9000/api/v1/build_order` returns the correctly sorted JSON array.