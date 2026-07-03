You are an open-source maintainer reviewing a broken PR for a lightweight, Bash-based CI/CD webhook server. 

The webhook server processes incoming REST API POST requests to trigger CI builds. However, the current implementation in the PR (`/home/user/pr/server.sh`) is broken in several ways:
1. It is vulnerable to command injection and crashes when handling unexpected characters (failing property-based testing).
2. It lacks proper authentication. The expected authorization token is an English phrase spoken in an audio file attached to the PR.
3. It has terrible performance and fails to handle concurrent requests efficiently.

Your task is to fix and optimize the webhook server. 

Step 1: Authentication Retrieval
The authorization token is the exact transcribed phrase spoken in `/app/auth_token.wav` (lowercase, no punctuation). 

Step 2: API Server Refactoring
Edit or rewrite `/home/user/pr/server.sh`. You must build a robust HTTP server in Bash (you may use tools like `socat` or `nc` combined with standard bash utilities).
The server must listen on `127.0.0.1:8080`.
It must accept `POST /webhook` requests.
It must validate the `Authorization: Bearer <transcribed_token>` header. If missing or incorrect, return `401 Unauthorized`.
It must read a JSON payload: `{"repo": "name", "branch": "name"}`.
It must NOT be vulnerable to command injection. For valid requests, it should echo "Build triggered for repo: <repo> on branch: <branch>" as the HTTP response body (with a `200 OK` status).

Step 3: Performance & Robustness
The server will be evaluated using an aggressive benchmarking and fuzzing suite. It must handle concurrent requests without dropping connections and successfully reject malicious payloads safely. 

Run your server in the background so it binds to port 8080. Leave it running as we will test it automatically.