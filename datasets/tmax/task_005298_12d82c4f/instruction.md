I have a messy data processing project in `/home/user/project` that needs to be properly organized, patched, built, and exposed via a reverse proxy. 

Please perform the following operations:

1. **Patch Processing:** 
   There is a buggy script at `/home/user/project/processor.py` and a patch file at `/home/user/project/fixes.patch`. Apply the patch to `processor.py`.

2. **Compilation and Linking:**
   The project includes a C file at `/home/user/project/cruncher.c`. Compile it into a shared library named `libcruncher.so` inside the `/home/user/project` directory. The patched `processor.py` relies on this shared object via `ctypes`.

3. **Package & Dependency Management:**
   Organize the project into a proper installable Python package. Create a `pyproject.toml` in `/home/user/project` using `setuptools` as the build backend. Name the package `data_org`. It must specify `Flask` and `gunicorn` as dependencies. 
   Create a virtual environment at `/home/user/venv`. Install the package into this virtual environment.

4. **Service Execution:**
   Start the application using `gunicorn` from your virtual environment, binding it to `127.0.0.1:5000`. Run it in the background so you can continue executing commands. The Flask app object is named `app` inside `processor.py`.

5. **Reverse Proxy Configuration:**
   Create an Nginx configuration file at `/home/user/nginx.conf`. It must:
   - Run as the current user (do not use `user` directive).
   - Listen on port `8080`.
   - Reverse proxy any requests coming to the `/api/` path to the gunicorn server at `http://127.0.0.1:5000/`. Note: The Flask app expects the path `/process`, so the proxy should rewrite `/api/process` to `/process` or simply pass the URI such that `http://127.0.0.1:8080/api/process` reaches the Flask route `/api/process` (the patch updates the Flask route to `/api/process`).
   - Store access logs at `/home/user/nginx_access.log`.
   - Store error logs at `/home/user/nginx_error.log`.
   - Store its pid at `/home/user/nginx.pid`.
   - Set `client_body_temp_path`, `proxy_temp_path`, `fastcgi_temp_path`, `uwsgi_temp_path`, and `scgi_temp_path` to `/tmp/` to avoid permission issues.
   Start Nginx in the background using this configuration: `nginx -c /home/user/nginx.conf`.

6. **Verification:**
   Once both services are running, make a GET request to `http://127.0.0.1:8080/api/process?data=helloworld` using `curl`. Save the raw JSON response exactly as returned to `/home/user/final_output.json`.