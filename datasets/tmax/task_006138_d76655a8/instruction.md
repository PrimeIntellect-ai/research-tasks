You are acting as a deployment specialist managing a microservice environment. We don't have a container daemon available, so we are simulating zero-downtime blue/green deployments using Bash scripts, background processes, and symlinks.

Your objective is to build the directory structure, create the service scripts with specific configurations and permissions, start the initial version (v1), and then write and execute a deployment script that safely transitions to the new version (v2).

Please complete the following phases:

**Phase 1: Directory Structure and Links**
Create the following directory structure:
- `/home/user/microservice/releases/v1`
- `/home/user/microservice/releases/v2`
- `/home/user/microservice/shared`

Create a symlink at `/home/user/microservice/current` that initially points to `/home/user/microservice/releases/v1`.

**Phase 2: Configuration and Permissions**
1. In `/home/user/microservice/releases/v1`, create a file named `config.ini` with the exact content: `MODE=blue`
2. In `/home/user/microservice/releases/v2`, create a file named `config.ini` with the exact content: `MODE=green`
3. Restrict permissions on both `config.ini` files so they are read-only for the owner, with no permissions for group or others (i.e., `0400`).

**Phase 3: The Microservice Script**
In both `v1` and `v2` directories, create an executable bash script named `worker.sh`. 
The script must do the following:
1. Trap the `SIGTERM` signal. When a `SIGTERM` is received, it must immediately append the exact line `Shutting down gracefully` to `/home/user/microservice/shared/app.log`, and then `exit 0`.
2. Source the `config.ini` file located in its own directory.
3. Enter an infinite loop where it:
   - Appends the exact line `Heartbeat: $MODE` (evaluating the variable from the config) to `/home/user/microservice/shared/app.log`.
   - Sleeps for 1 second.

**Phase 4: Rolling Deployment**
1. Manually start the v1 worker in the background by navigating to `/home/user/microservice/current` and executing `./worker.sh &`. Let it run for at least 2 seconds so it registers some heartbeats.
2. Write a deployment script at `/home/user/microservice/deploy.sh`. This script must:
   - Atomically update the symlink `/home/user/microservice/current` to point to `/home/user/microservice/releases/v2`.
   - Start the new worker (v2) from the updated `current` directory in the background.
   - Find the process ID (PID) of the old v1 `worker.sh` and send it a `SIGTERM` signal.
   - Wait for the old process to completely terminate.
   - Write the exact line `Deployment of v2 successful` to `/home/user/microservice/shared/deploy.log`.
3. Execute `/home/user/microservice/deploy.sh`.
4. Wait 2 seconds, then kill all remaining background `worker.sh` processes so the automated tests can safely inspect the logs.

Ensure all paths are absolute and exactly match the instructions.