You are an open-source maintainer reviewing a broken Pull Request (PR) for a custom API Gateway project. The PR aims to introduce a new schema for the backend API and add a streaming log redactor to sanitize sensitive tokens before they hit the disk. However, the PR author left the redactor incomplete, the multi-service configuration broken, and the schema patch has merge conflicts.

Your task is to fix the PR and ensure the end-to-end system works.

**1. Fix the Schema Migration (Diff/Patch Processing)**
The PR author provided a patch file at `/home/user/schema_update.patch`. This patch is supposed to update the backend schema located at `/app/schema.json`.
- The patch currently fails to apply due to a simulated merge conflict.
- Manually inspect the patch, resolve the conflict so that the new schema includes BOTH the `email` field (from the base schema) and the new `api_key` field (from the PR), and apply it to `/app/schema.json`.

**2. Implement the Streaming Redactor (State Machine / Parser)**
The gateway logs requests to standard output, but we need to redact sensitive data. The PR author left an empty executable file at `/home/user/redactor`.
- Write a program in `/home/user/redactor` (you can use Bash, Awk, Python, etc., but it must be executable and process `stdin` to `stdout`).
- The input consists of log lines in the format: `[TIMESTAMP] IP_ADDRESS key1=value1 key2=value2 ...`
- You must construct a parser/state machine that finds any key named exactly `secret_token` and replaces its value with `***`.
- **Crucial parsing rule:** Values may contain spaces if they are escaped with a backslash (e.g., `secret_token=my\ secret\ val key3=foo`). Your parser must correctly identify the end of the value (an unescaped space or the end of the line) and redact the entire value, preserving the rest of the line exactly.
- Example Input: `[2023-10-10T12:00:00] 127.0.0.1 user=admin secret_token=ab\ cd\ ef status=200`
- Example Output: `[2023-10-10T12:00:00] 127.0.0.1 user=admin secret_token=*** status=200`

**3. Fix the End-to-End Orchestration (Multi-Service Compose)**
The system consists of two services managed by a startup script:
- **Gateway:** Listens on `127.0.0.1:8000`
- **Backend:** Listens on `127.0.0.1:8001`
Currently, the gateway is configured to use `/bin/cat` as its log filter.
- Edit the configuration file at `/app/gateway.conf` and change the `REDACTOR_CMD` variable to point to your new redactor: `/home/user/redactor`.
- Restart the gateway service by running `/app/restart_gateway.sh`.
- Verify the end-to-end flow by sending a test curl `POST` request to `http://127.0.0.1:8000/log` with a JSON payload `{"secret_token": "test"}`. Ensure the logs generated in `/home/user/gateway.log` correctly reflect the redacted output.