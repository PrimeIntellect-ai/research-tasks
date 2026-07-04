You are a site administrator tasked with fixing a local deployment of two microservices that act as our internal CI/CD trigger system. 

Currently, the setup is broken due to a misconfiguration in how the services communicate (simulating a network/routing misconfiguration) and broken user account records. Furthermore, we need to enforce proper log rotation for compliance.

Here is the current state of the system in `/home/user/app/`:
1. `/home/user/app/users.json`: A configuration file managing application user accounts. It is currently missing the required `ci_worker` user and has a syntax error.
2. `/home/user/app/auth_service.py`: A Python service running on port 8081 that authenticates users. It currently logs to a single file without rotation.
3. `/home/user/app/data_service.py`: A Python service running on port 8082 that triggers CI deployments. It expects a specific header from the auth service, but they are mismatched.

Your tasks are as follows:

1. **Fix User Accounts**:
   Edit `/home/user/app/users.json`. Fix the JSON syntax. Add a new user with the username `ci_worker`, password `ci_secure_pass`, and role `builder`.

2. **Fix Service Communication**:
   The `data_service.py` service expects the authenticated username to be passed in the `X-Internal-User` header. However, `auth_service.py` is currently forwarding the username in the `X-Forwarded-User` header. Modify `auth_service.py` so it forwards the username using the `X-Internal-User` header instead when proxying requests to the data service.

3. **Configure Log Rotation**:
   Modify `auth_service.py`'s logging configuration. Replace the standard `FileHandler` with a `logging.handlers.TimedRotatingFileHandler`. It must log to `/home/user/app/logs/auth.log`, rotate at `'midnight'`, and keep a `backupCount` of `5`.

4. **Construct the CI/CD Pipeline Script**:
   Create a bash script at `/home/user/run_pipeline.sh` that simulates our CI process. The script must:
   - Use `curl` to send a POST request to `http://localhost:8081/login` with JSON payload `{"username": "ci_worker", "password": "ci_secure_pass"}`.
   - Extract the `token` from the JSON response.
   - Use `curl` to send a POST request to `http://localhost:8081/trigger` with the header `Authorization: Bearer <token>`. (The auth service proxies this to the data service).
   - Save the raw HTTP response body of the `/trigger` request into `/home/user/build_result.txt`.

Ensure `/home/user/run_pipeline.sh` is executable. You do not need to keep the services running in the background after you finish testing your solution.