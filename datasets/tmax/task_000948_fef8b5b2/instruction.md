You are a Linux Systems Engineer responsible for hardening and deploying a newly developed internal Git notification daemon.

We have a vendored third-party Python package located at `/app/git-notifier-2.0.0`. This package provides a simple HTTP server that triggers internal workflows when it receives webhook requests. 

However, during a security audit, we found several issues that you need to fix:
1. The daemon currently ignores configuration variables and hardcodes its listening address to `0.0.0.0:8000`. You must modify the source code so that it binds to the host and port specified by the `BIND_HOST` and `BIND_PORT` environment variables.
2. The daemon is supposed to check for an authorization token, but there is a typo in the code preventing it from reading the correct environment variable. Fix it so it properly reads `AUTH_TOKEN`.
3. After fixing the code, set up a Python virtual environment at `/home/user/venv` and install the package.

Once the package is fixed and installed, perform the following infrastructure setup:

**A. Service Configuration**
Create a wrapper script at `/home/user/start-daemon.sh` that:
- Activates the virtual environment.
- Exports `BIND_HOST=127.0.0.1` and `BIND_PORT=8080`.
- Exports `AUTH_TOKEN=secure_admin_99`.
- Starts the `git-notifier` server in the background.
Run this script to ensure the daemon is listening.

**B. Git Server & Hooks**
- Initialize a bare Git repository at `/home/user/target.git`.
- Create a `post-receive` hook in this repository. When code is pushed, the hook must execute a shell command (using `curl` or python) that sends an HTTP POST request to `http://127.0.0.1:8080/notify`.
- The request must include the header `Authorization: Bearer secure_admin_99` and a JSON body `{"event": "push"}`.

**C. Port Forwarding**
External systems cannot reach port 8080 directly due to local firewall simulation rules. They expect to communicate over port `9090`.
- Use `socat` to create a persistent local port forward that listens on TCP port `9090` and forwards all traffic to `127.0.0.1:8080`.
- Run this in the background so it remains active.

Ensure all services (the python daemon and the socat forwarder) are running and the Git hook is executable. Automated verifiers will test pushing to your Git repository and making direct protocol requests to port 9090.