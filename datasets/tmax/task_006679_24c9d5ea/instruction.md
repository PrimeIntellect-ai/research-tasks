You are a network engineer tasked with troubleshooting and fixing a custom, lightweight staged deployment pipeline. The previous engineer left the project incomplete. You need to write a Git hook and a proxy router to complete the system.

The system consists of a Git repository that, upon receiving a push, deploys a static website to a new directory, spins up an HTTP server on an alternating backend port, and updates a proxy script to route frontend traffic to the new version.

Your objective is to implement the following components strictly using Python and standard bash utilities:

1. **Storage-Aware Deployment Hook:**
Create a Git post-receive hook at `/home/user/repo.git/hooks/post-receive`. It must be an executable Python script (`#!/usr/bin/env python3`) that reads lines from standard input (format: `old_rev new_rev refname`). For every push, it must:
- Calculate the total size (in bytes) of all files in `/home/user/deployments/`.
- If the total size exceeds 500,000 bytes, print exactly "Storage quota exceeded" to standard error and exit with code 1.
- If storage is fine, extract the pushed `new_rev` tree into a new directory named `/home/user/deployments/<new_rev>`.
- Read the port number from `/home/user/active_port.txt`. If the file doesn't exist or is empty, default to active port 9002.
- Determine the *new* backend port: if the active port was 9001, the new port must be 9002. If it was 9002, the new port must be 9001.
- Start a background Python HTTP server serving the newly extracted directory (`/home/user/deployments/<new_rev>`) on the new backend port. (e.g., using `python3 -m http.server`).
- Overwrite `/home/user/active_port.txt` with the new port number.

2. **Dynamic Forwarding Router:**
Write a Python script at `/home/user/router.py` that acts as a frontend HTTP proxy listening on port `8080`.
- It must read the active backend port from `/home/user/active_port.txt`.
- It must accept incoming TCP connections on `127.0.0.1:8080` and forward the raw HTTP traffic to `127.0.0.1:<active_port>`.
- **Robustness requirement:** If `/home/user/active_port.txt` is missing, or if the connection to the backend port is refused, the proxy must catch the error and respond to the frontend client with a raw HTTP 503 response: `HTTP/1.1 503 Service Unavailable\r\n\r\nBackend offline` and gracefully close the connection without crashing.
- The router should run indefinitely. You should test it in the background while working.

**Pre-existing Environment:**
- A bare Git repository exists at `/home/user/repo.git`.
- A clone of this repository exists at `/home/user/workspace`.
- The directory `/home/user/deployments` exists.

**Verification:**
To test your work, ensure `router.py` is running in the background. Go to `/home/user/workspace`, add an `index.html` file with the content `v1`, commit, and push it to `origin master`. A subsequent `curl -s http://127.0.0.1:8080/index.html` should return `v1`.

Do not modify the `workspace` or push anything as your final state. We will perform our own test pushes during verification. Make sure `/home/user/router.py` is robust and `/home/user/repo.git/hooks/post-receive` is marked executable.