You are the site administrator for a system that automatically provisions user account workspaces based on file-drop requests. You need to implement a small automated pipeline using Rust and bash. 

Your objective is to create a filesystem-based worker, a process supervisor, and a mini CI/CD deployment script.

Please complete the following steps:

1. **The Rust Worker**:
Create a new Rust project in `/home/user/user-mngr`. Write a program that does the following when executed:
- Checks if the file `/home/user/queue/request.txt` exists.
- If it exists, reads the file. The file contains a list of usernames, one per line.
- For each username, creates a directory at `/home/user/homes/<username>`.
- Inside each new user directory, creates a file named `readme.txt` containing exactly the text: `Welcome <username>` (replace `<username>` with the actual name).
- Finally, deletes `/home/user/queue/request.txt` so the request is not processed again.
- If the file does not exist, the program should just exit successfully without errors.

2. **The Supervisor Script**:
Write a bash script at `/home/user/run_service.sh`. This script will act as a process supervisor:
- It should run in an infinite loop.
- Inside the loop, it must execute the compiled binary located exactly at `/home/user/bin/user-mngr`.
- After the binary exits, the loop should `sleep 1` before repeating.
- Ensure the script has execute permissions.

3. **The Mini CI/CD Deployment Script**:
Write a bash script at `/home/user/deploy.sh` that automates building and deploying the worker:
- It should navigate to `/home/user/user-mngr` and run `cargo build --release`.
- If the build fails, the script should exit with an error.
- If the build succeeds, it must create `/home/user/bin/` (if it doesn't exist) and copy the compiled binary to `/home/user/bin/user-mngr`.
- It must then find any currently running instance of `/home/user/run_service.sh` and terminate it safely.
- Finally, it must start `/home/user/run_service.sh` in the background (detached so `deploy.sh` can exit while the service keeps running).
- Ensure the script has execute permissions.

Ensure everything functions correctly. To verify your work, you can run `/home/user/deploy.sh`, drop a test `request.txt` into `/home/user/queue/`, and observe if the user homes are generated.