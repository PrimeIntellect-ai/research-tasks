Can you help me fix our failing build and deployment? The project is located at `/home/user/app`. It consists of a FastAPI web frontend, a Redis caching layer, and a Python background worker. 

Currently, when I run `/home/user/app/start.sh`, the build fails and the services do not start correctly. Here is what we know:
1. **Git History Forensics**: A developer recently removed a hardcoded `API_SECRET` from `worker/config.py` because it was a security risk, but they broke the build in the process. The background worker now crashes on startup because it expects this secret. You need to find the deleted `API_SECRET` in the git repository's history and provide it to the worker via an environment variable named `API_SECRET` in the startup script.
2. **Memory Dump Analysis**: The web frontend requires an initialization token (`INIT_TOKEN`) to accept API requests. A previous instance crashed and left a core dump at `/home/user/app/frontend_crash.dump`. You need to extract this token from the dump file. The token is a 32-character alphanumeric string prefixed with `TOKEN-`. Once found, supply it as the `INIT_TOKEN` environment variable in the startup script.
3. **Service Configuration**: The FastAPI service is failing to connect to Redis. Inspect the logs or the startup script and fix the connection details. Both the web server and the worker must be able to communicate with the Redis instance.

Your goal is to:
1. Fix `/home/user/app/start.sh` so that it successfully starts Redis, the FastAPI web server, and the background worker.
2. Ensure the FastAPI web server is listening on `127.0.0.1:8080`.
3. Ensure the Redis server is correctly configured and bound to the port the applications expect.
4. Leave the services running in the background. Do not exit the processes. 

Once you have fixed the setup and started the services, please write a summary of the bugs you fixed to `/home/user/app/debugging_report.txt`. An automated test will verify the fix by sending HTTP requests to the FastAPI server using the recovered credentials.