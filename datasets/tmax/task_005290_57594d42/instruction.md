You are tasked with resolving a severe resource leak in our vendored bash-based web server. Recently, our production environment has been experiencing runaway CPU usage and process starvation. We suspect this is due to lingering background processes (process leaks) triggered by malformed HTTP requests.

The server source code is a vendored package located at `/app/bash-http-server`. This repository contains exactly 200 commits. The regression was introduced recently, but we do not know exactly which commit caused it.

Your objectives:
1. **Identify the bad commit:** Reconstruct the timeline and use `git bisect` (or any script you write) within `/app/bash-http-server` to find the exact commit hash that introduced the process leak. The leak is triggered when a request is made to the `/compute` endpoint with a specific malicious `User-Agent` header (you will need to do some light fuzzing to find what triggers the infinite loop). Write the full 40-character commit hash of the bad commit to `/home/user/bad_commit.txt`.
2. **Fix the code:** Analyze `server.sh` and fix the root cause of the process leak so that malicious or dropped requests do not leave orphaned background loops.
3. **Deploy the fixed service:** Start your fixed server on `127.0.0.1:9090` and leave it running in the background. It must accept incoming HTTP connections.

Requirements:
- The server must respond to `GET /` with a `200 OK` status and the body `OK`.
- The server must handle requests to `GET /compute` without leaking any background processes, regardless of the `User-Agent` provided.
- Ensure the server is actively listening on `127.0.0.1:9090` when you finish.