You are a performance engineer tasked with debugging a microservice application that has recently experienced severe performance degradations and crashes. 

The application consists of two services:
1. A Python-based API gateway (`/app/frontend`) 
2. A Node.js backend worker (`/app/backend`)

A colleague left an architecture diagram at `/app/architecture.png` that specifies the exact port numbers each service must bind to. You will need to extract the `FRONTEND_PORT` and `BACKEND_PORT` from this image (tesseract is installed) to configure the services properly.

Here is your workflow:
1. **Extract Configuration:** Read the ports from `/app/architecture.png`.
2. **Regression Hunting:** The Node.js backend service currently hangs on certain requests due to an infinite loop. Use `git bisect` in `/app/backend` to identify the specific commit that introduced this regression. The known good commit is `v1.0` and the current `HEAD` is bad. 
3. **Fix the Loop:** Once you find the bad commit, fix the infinite loop bug in the `worker.js` file, commit your fix, and leave the repository on the `main` branch with your fix applied.
4. **System Trace:** The Python frontend service is currently crashing on startup. Use system call tracing (`strace`) to figure out why it's failing to start and fix the issue in `server.py`. 
5. **Start Services:** Start both services in the background so they are ready to receive traffic. The frontend must listen on `FRONTEND_PORT` and the backend on `BACKEND_PORT`. 
6. **Reporting:** Write the full SHA of the bad commit you found in the backend repository to `/app/bad_commit.txt`.

The automated verifier will issue an HTTP GET request to the frontend's `/status` endpoint, and a direct TCP payload (`ping`) to the backend service. Ensure both services are running and correctly returning successful responses before finishing.