Hello IT Support,

We have an urgent ticket (TICKET-9921) regarding the migration of our legacy data transformation service.

Historically, we used a compiled C binary located at `/app/legacy_transformer` to parse our custom pipe-and-colon delimited data formats into JSON. We are trying to replace this with a modern Python web service, the source code of which is located in the Git repository at `/home/user/ticket_repo`.

Unfortunately, the migration has hit several snags, and the original developer is on leave. Your task is to resolve the following issues and get the new service running:

1. **Dependency/Environment Failure:** The Python service currently fails to start due to a dependency conflict in its `requirements.txt` and a missing environment variable misconfiguration. You need to repair the environment, resolve the conflicts, and ensure the dependencies can be cleanly installed.
2. **Regression in Data Transformation:** The Python service is returning incorrect JSON for certain edge cases compared to the legacy binary. We suspect a recent commit introduced this regression. Use `git bisect` or your preferred debugging method to identify the bad commit. 
3. **Fuzzing and Diff Analysis:** You must reverse-engineer the exact expected behavior of the `/app/legacy_transformer` binary (it acts as a black-box oracle reading from stdin and writing to stdout). You should script a fuzzing test to find inputs where the Python logic differs from the legacy binary, and fix the Python code so its output is a 100% exact match to the legacy binary.
4. **Deployment:** Once fixed, start the Python HTTP service. It must listen on `127.0.0.1:8080`.

**Service Requirements:**
- The service must expose a `POST /transform` endpoint.
- The endpoint accepts raw text data in the request body.
- It must return the exact JSON payload that `/app/legacy_transformer` would generate for the same input, with a `200 OK` status.
- Ensure the service runs in the background or occupies your final terminal session so it remains up for verification.

Please troubleshoot, fix the repository, and start the service.