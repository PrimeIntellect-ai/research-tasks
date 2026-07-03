You are an infrastructure engineer troubleshooting a broken connectivity setup. We are using a custom C-based lightweight gateway called `net-bridge-c`. It is failing to compile, ignores its configuration, and is completely unreliable when deployed. 

Your task is to fix the gateway's source code, configure its environment using precise directory structures and symlinks, and write a robust process supervisor in bash to keep it running.

**Step 1: Fix the Vendored Package**
A vendored copy of the gateway source is located at `/app/net-bridge-c/`. 
1. The `Makefile` is broken and fails to build the project. Identify the missing compilation flags (it requires threading) and fix it.
2. The source code in `src/gateway.c` has a deliberate hardcoded bug. It ignores the `BIND_PORT` environment variable and defaults to a wrong port. Modify the C code so that it correctly reads the `BIND_PORT` environment variable using `getenv()` and `atoi()` to set the listening port. 
3. Run `make` to produce the `gateway` executable inside `/app/net-bridge-c/`.

**Step 2: Environment Setup**
1. Create the following directory structure:
   - `/home/user/gw/logs`
   - `/home/user/gw/conf`
   - `/home/user/gw/run`
2. Create a configuration file at `/home/user/gw/conf/settings.ini` containing exactly the following line:
   `target=127.0.0.1:9090`
3. Create a symlink at `/home/user/gw/active_conf` that points to `/home/user/gw/conf/settings.ini`.

**Step 3: Write a Supervisor Script**
The gateway frequently crashes, so it must be supervised.
Create a bash script at `/home/user/supervisor.sh` that does the following in an infinite loop:
1. Starts the `/app/net-bridge-c/gateway` executable.
2. Passes the configuration file via an environment variable `CONFIG_PATH=/home/user/gw/active_conf`.
3. Sets the environment variable `BIND_PORT=8888`.
4. Redirects both stdout and stderr of the gateway to `/home/user/gw/logs/gw.log`.
5. Writes the PID of the running gateway process to `/home/user/gw/run/gw.pid`.
6. `wait`s for the process to exit.
7. If the process exits, copies the current log file to `/home/user/gw/logs/gw.log.bak.<timestamp>` (where `<timestamp>` is the current Unix epoch time, e.g., output of `date +%s`).
8. Instantly restarts the gateway.

**Step 4: Execution**
Ensure your supervisor script is executable and run it in the background:
`nohup /home/user/supervisor.sh &`

Automated verifiers will send HTTP requests to the gateway on port `8888`, deliberately trigger a crash, and verify that the supervisor successfully backs up the log and restores the service.