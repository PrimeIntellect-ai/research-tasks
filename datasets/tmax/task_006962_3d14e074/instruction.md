You are tasked with diagnosing and fixing a deployment environment for a multi-language application. A background worker service and a simple reverse proxy were supposed to be running, but they are failing to start or are writing corrupted data to the wrong locations due to environment issues (similar to cron job PATH/environment mismatches).

Your objective is to write an idempotent configuration script `/home/user/deploy.sh` that fixes the environment, directory structures, and starts the services correctly.

Here are the requirements for your script and the system state it must achieve:

1. **Directory & Link Management:**
   - The application has releases in `/home/user/releases/v1` and `/home/user/releases/v2` (these already exist).
   - Your script must idempotently ensure that a symlink `/home/user/app_current` points to `/home/user/releases/v2`. 
   - Ensure the directory `/home/user/logs` exists.

2. **Environment & Locale Configuration (The Fix):**
   - The application expects to run with a specific timezone and locale to format currency and timestamps correctly, but currently defaults to UTC and POSIX.
   - You must create a wrapper script `/home/user/start_worker.sh` that, when executed, sets the environment variables `TZ=Europe/Berlin` and `LC_ALL=en_US.UTF-8`.
   - The wrapper script must explicitly change the working directory to `/home/user/logs` before executing `/home/user/app_current/worker.py` in the background, so that its relative log file (`worker_output.log`) is written to `/home/user/logs/worker_output.log`.
   - Redirect standard output and error of `worker.py` to `/home/user/logs/worker_output.log`.

3. **Reverse Proxy Setup:**
   - You need to set up a simple user-space reverse proxy using `socat`.
   - Your `deploy.sh` script must write a script at `/home/user/start_proxy.sh` that launches `socat` to listen on TCP port `8080` and forward all traffic to TCP port `8081` (where the worker will eventually listen).
   - Ensure `start_proxy.sh` is executable.

4. **Idempotency:**
   - The `/home/user/deploy.sh` script must be completely idempotent. If run multiple times, it should not fail, duplicate data, or create nested symlinks.

5. **Execution:**
   - Write the `/home/user/deploy.sh` script, make it executable, and execute it yourself. 
   - Then, execute `/home/user/start_worker.sh` and `/home/user/start_proxy.sh` to ensure the files are generated and the state is correct. (You do not need to keep the processes running indefinitely for the final check, but the scripts and configurations must exist and be correct).

Do not use `sudo` or require root privileges. All operations should be confined to `/home/user`.