I am migrating an old legacy numerical computation microservice from Python 2 to Python 3. I need your help to fix the legacy vendored dependency, port the web server, fix a known memory leak, and get the service running.

Here are the requirements:

1. **Vendored Package Configuration:**
   We rely on a proprietary local package called `py2num`. The source code for this package is located at `/app/vendored/py2num`. 
   Since this was written for Python 2, it currently fails to install and run in Python 3. You must fix the compatibility issues in the package (syntax errors, obsolete built-ins, etc.) so that it can be installed in our Python 3 environment.
   Once you have fixed it, install the package into the current environment. 
   Additionally, you must generate a unified diff patch of your changes to the `py2num` package and save it to `/home/user/py2num_migration.patch`.

2. **Web Service Porting and Memory Profiling:**
   The legacy web server code is located at `/home/user/server.py`. It provides a simple API that uses `py2num` to compute the sum of squares up to `n`.
   - Update `server.py` to be strictly Python 3 compatible.
   - We observed a severe memory leak in `server.py` when it processes large values of `n`. You need to profile the memory usage and fix the memory leak. The service must be able to handle hundreds of requests for `n = 5000000` without exceeding 100MB of RAM usage. Modify `server.py` to fix this algorithmic or structural leak.

3. **API Specifications:**
   The updated `server.py` must run a persistent HTTP server listening on `127.0.0.1:8080`.
   - **Endpoint:** `POST /compute`
   - **Authentication:** All requests must include the HTTP header: `X-Migration-Auth: 99887766`
   - **Payload:** JSON format, e.g., `{"n": 100}`
   - **Response:** JSON format, e.g., `{"result": 338350}` (for `n=100`, returning the sum of squares).
   - If the authentication header is missing or incorrect, return a `401 Unauthorized` status.
   - If the payload is invalid, return a `400 Bad Request`.

Start the service in the background and leave it running. Write a log file of the startup to `/home/user/server.log` so I know it has started successfully.