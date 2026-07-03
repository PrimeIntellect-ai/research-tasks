You are acting as a container specialist managing a lightweight deployment workflow for microservices. You need to set up a local Git-based deployment system that automatically restarts a Python microservice whenever new code is pushed.

Please complete the following steps exactly as specified. All work should be done within `/home/user`.

1. **Environment Setup**: 
   Create a file at `/home/user/env.sh` containing exactly:
   `export APP_PORT=8282`

2. **Git Repository Setup**:
   Create a bare Git repository at `/home/user/app.git`.

3. **Git Hook (Python)**:
   Write a `post-receive` hook in Python at `/home/user/app.git/hooks/post-receive`. Ensure it is executable.
   When triggered, this hook must:
   - Check out the latest code from the `main` branch to the directory `/home/user/app_run` (create this directory if it doesn't exist).
   - Read the `APP_PORT` value by parsing `/home/user/env.sh`.
   - Find and gracefully terminate any existing process listening on `APP_PORT`.
   - Execute the deployed `app.py` in the background (e.g., `python3 /home/user/app_run/app.py &`) with the environment variable `APP_PORT` set to the value read.

4. **Service Creation and Deployment**:
   - Clone the bare repository to `/home/user/app_src`.
   - In `/home/user/app_src`, write a Python script named `app.py`. This script should start a basic HTTP server listening on the port specified by the `APP_PORT` environment variable. When it receives a GET request at `/`, it must respond with the exact plain text string: `MICROSERVICE_V1_ACTIVE`.
   - Commit `app.py` to the `main` branch and push it to the bare repository (`origin main`).

5. **Verification**:
   After the push successfully triggers the hook and starts the microservice, wait a couple of seconds, and then issue a `curl` request to `http://localhost:8282/`. 
   Save the standard output of this `curl` command to `/home/user/result.log`.

Ensure all paths, filenames, and response strings match these instructions perfectly. Do not use root privileges.