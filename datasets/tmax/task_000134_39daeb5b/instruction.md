You are a container specialist managing a set of microservices. We need to build a user management microservice and implement a rolling, staged deployment script for it. All tasks should be completed within `/home/user`.

Follow these steps exactly:

**Phase 1: Interactive User Administration Script**
1. Write a Python script named `/home/user/user_manager.py` that manages an SQLite database at `/home/user/app.db`.
2. The script must initialize the database on its first run, creating a table named `users` with columns `username` (TEXT) and `role` (TEXT).
3. The script must accept two command-line arguments to add a user: `python3 user_manager.py add <username> <role>`. 
4. Using your script, add the following three users to the database:
   - username: `alice`, role: `admin`
   - username: `bob`, role: `dev`
   - username: `charlie`, role: `dev`

**Phase 2: The Microservice API**
1. Write a Python script named `/home/user/api.py`.
2. This script must start a basic HTTP server using Python's standard `http.server` library.
3. It should accept a single command-line argument for the port number (e.g., `python3 api.py 8081`).
4. It must respond to `GET /users` by returning a JSON representation of all users in `app.db` with the format: `[{"username": "alice", "role": "admin"}, ...]`. Ensure the `Content-Type` is set to `application/json`.

**Phase 3: Staged Deployment Script**
1. Write a bash script named `/home/user/deploy.sh` that implements a basic staged/blue-green deployment.
2. The script must read `/home/user/active_port.txt`. If the file doesn't exist, assume the current active port is `8080`.
3. Determine the *new* port: if the current active port is `8080`, the new port must be `8081`. If the current active port is `8081`, the new port must be `8080`.
4. Start a new instance of `api.py` in the background on the *new* port.
5. Wait up to 5 seconds, repeatedly checking (e.g., using `curl -s`) if the new instance responds with HTTP 200 at the `/users` endpoint.
6. If the new instance is healthy:
   - Kill the *old* `api.py` process (you may rely on `/home/user/active_pid.txt` from previous deployments, or find it dynamically).
   - Write the *new* port to `/home/user/active_port.txt`.
   - Write the *new* process ID to `/home/user/active_pid.txt`.
7. If the new instance fails to become healthy within 5 seconds, kill the new instance, output an error, and exit with a non-zero status (leaving the old instance untouched).

**Phase 4: Execution and Verification**
1. Run `/home/user/deploy.sh`. (Since there is no previous deployment, this will deploy to port 8081 and update the tracking files).
2. Run `/home/user/deploy.sh` a second time. (This will deploy to port 8080, verify it, kill the 8081 instance, and update tracking files).
3. Finally, query the active API using `curl` and save the output to `/home/user/deployment_test.json`.