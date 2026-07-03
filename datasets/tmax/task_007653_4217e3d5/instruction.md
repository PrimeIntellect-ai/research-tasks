You are a systems programmer and backend engineer. We have a small project located in `/home/user/app` that consists of a C library, a Python REST API, and a reverse proxy requirement. Currently, the system is broken on multiple levels.

Your task is to fix the issues, start the services, and write a test to verify the system.

Here is the current state of `/home/user/app`:
1. `libcalc.c`: Contains a simple C function `int calculate(int n);`
2. `Makefile`: Intended to build a shared library `libcalc.so` from `libcalc.c`. However, there is a linking/compilation issue—it doesn't produce a valid shared object that Python's `ctypes` can load.
3. `api.py`: A Flask application that exposes a REST endpoint `/compute`. It loads `libcalc.so`. However, it currently fails to load the library due to the build issue. Furthermore, there is a severe memory leak in `api.py` that causes it to consume ~1MB of memory per request.

Perform the following steps:
1. **Fix the C library linking issue:** Modify `/home/user/app/Makefile` so that `make` successfully builds a valid shared library `libcalc.so`. Run `make`.
2. **Fix the Memory Leak:** Inspect `/home/user/app/api.py`. Find and remove the memory leak in the REST endpoint while ensuring it still returns the correct calculation.
3. **Configure Reverse Proxy:** Create a valid Nginx configuration file at `/home/user/app/nginx.conf`. It must start an HTTP server listening on `127.0.0.1:8080` and proxy all requests to the Flask app running at `127.0.0.1:5000`. Start the nginx reverse proxy in the background using this specific config file (e.g., `nginx -c /home/user/app/nginx.conf`).
4. **Start the API:** Start `api.py` in the background.
5. **Write a Test Script:** Create a Python script at `/home/user/app/test.py` that:
   - Makes 10 HTTP GET requests to the reverse proxy: `http://127.0.0.1:8080/compute?val=21`
   - Asserts that every response is `42`.
   - If successful, writes the exact string `Proxy and API functional` to `/home/user/app/success.log`.

Run your test script to generate the log file.