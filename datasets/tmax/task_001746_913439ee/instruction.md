You are a platform engineer responsible for maintaining a dynamic CI/CD pipeline environment. We have a pipeline that uses a custom logic evaluation service to determine if specific build steps should run, but the system is currently broken and incomplete.

You must complete the following four objectives:

1. **Fix the C++ Project Linking:**
   There is a CMake project located at `/home/user/project`. It consists of a shared library `custom_math` and an executable `app`. Currently, the executable fails to build because it cannot find the shared library at link time. Modify the CMake configuration (specifically in `/home/user/project/src/CMakeLists.txt` or root `CMakeLists.txt`) so that the `app` target correctly links against the `custom_math` shared library and compiles successfully.

2. **Implement the Evaluation API (Python):**
   Write a Python web service (using Flask or FastAPI, whichever you prefer) in `/home/user/evaluator/app.py`. The service must run on `127.0.0.1:5000`. 
   - It must expose a `GET` endpoint at `/evaluate`.
   - It should accept a URL query parameter `expr`. The value will be a simple mathematical inequality string using basic operators (e.g., `expr=10-2>5` or `expr=3*3<10`).
   - The API must parse and evaluate this expression and return a JSON payload indicating whether the condition is met: `{"build": true}` if the inequality is mathematically true, and `{"build": false}` if it is false.

3. **Configure the Reverse Proxy:**
   Create a non-root Nginx configuration file at `/home/user/nginx.conf`. 
   - It must start a server listening on `127.0.0.1:8080`.
   - It must act as a reverse proxy, routing all requests to the Python evaluation service running on port `5000`.
   - Since you do not have root access, ensure your `nginx.conf` overrides default paths (like `pid`, logs, and temporary paths) to point to locations in `/tmp/nginx/` so Nginx can start successfully without permissions errors. Start Nginx in the background using your config.

4. **Write the Pipeline Trigger Script:**
   Write a bash script at `/home/user/run_pipeline.sh`.
   - The script must use `curl` to request `http://127.0.0.1:8080/evaluate?expr=7*2%3E10`.
   - It must parse the JSON response.
   - If `"build"` is `true`, the script must build the CMake project (using a build directory at `/home/user/project/build`), execute the resulting binary (`/home/user/project/build/src/app`), and save the exact standard output of the executable to `/home/user/pipeline_output.txt`.

Ensure your Python service and Nginx are running in the background before running your script.