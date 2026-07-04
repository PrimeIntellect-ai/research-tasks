You are a performance and forensics engineer responding to an incident. We have a multi-service text-processing pipeline that has been experiencing severe resource exhaustion and hangs. 

Our pipeline consists of two services:
1. An `nginx` reverse proxy listening on port 8080.
2. A custom C-based HTTP backend service (`backend`) listening on port 9000.

Currently, the system is completely broken in two ways:
First, the services are not glued together correctly. The Nginx configuration at `/home/user/nginx.conf` is misconfigured. When you run the startup script at `/app/start_services.sh`, Nginx starts, but requests to `http://localhost:8080/process` do not reach the C backend. You must fix `/home/user/nginx.conf` so that Nginx correctly proxies the `/process` endpoint to the C backend at `127.0.0.1:9000`. 

Second, the C backend (source located in `/home/user/backend/`) has a critical vulnerability. When it receives specific types of malformed or maliciously crafted payloads, a loop termination bug in the custom parsing logic prevents it from converging. The parsing loop spins infinitely, locking up the worker thread. Since the client eventually times out and cancels the request, the backend leaks these hanging threads permanently, leading to a complete Denial of Service.

Your objectives:
1. **Fix the Compose Setup**: Edit `/home/user/nginx.conf` so the end-to-end flow works. A clean HTTP POST request to `http://127.0.0.1:8080/process` should successfully return a 200 OK from the C backend. Restart the services as needed.
2. **Forensic Analysis & Minimization**: Debug `/home/user/backend/parser.c` to understand exactly what payload structure triggers the infinite loop. 
3. **Build a Detector**: We need a standalone C program to act as a sanitiser/pre-filter for incoming requests. Create a C source file at `/home/user/detector.c` and compile it to an executable at `/home/user/detector`. 
   - The detector must accept exactly one argument: the absolute path to a file containing a raw HTTP request. Example: `/home/user/detector /tmp/request.txt`
   - It must analyze the file's contents and determine if it contains the malicious pattern that triggers the backend's loop termination bug.
   - If the request is safe (clean), the detector MUST exit with code `0`.
   - If the request is malicious (evil) and would cause the hang, the detector MUST exit with code `1`.

For testing your detector, we have provided two corpora of raw HTTP requests:
- `/app/corpus/clean/`: Contains 50 valid requests.
- `/app/corpus/evil/`: Contains 50 requests that trigger the bug.

Your `/home/user/detector` binary must correctly classify 100% of both corpora. You do not need to patch the C backend itself for this task to be considered complete; your focus must be on diagnosing the root cause to build the perfect `detector`.