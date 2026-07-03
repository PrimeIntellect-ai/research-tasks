You are an SRE building a self-deploying uptime monitoring service using Rust and GitOps principles. Since you do not have root access, you will build a user-space deployment pipeline.

Your task consists of four parts. Complete them in order:

1. **Storage Configuration (Mock fstab):**
   You need a dedicated location for logs. Create an empty directory at `/home/user/mnt/logs`. 
   Create a configuration file at `/home/user/monitor.fstab` with exactly one line representing how you would mount a log directory. Use this exact format:
   `/home/user/logs_pool /home/user/mnt/logs none bind 0 0`
   Create the source directory `/home/user/logs_pool` as well.
   Write a bash script at `/home/user/mount_logs.sh` that parses `/home/user/monitor.fstab`. It should read the source and destination paths from the file and use `bindfs` to mount the source to the destination. (e.g., `bindfs <src> <dest>`).

2. **Git Deployment Hook:**
   Initialize a bare Git repository at `/home/user/sre-monitor.git`.
   Create a `post-receive` Git hook in this bare repository. The hook must:
   - Check out the pushed source code into a work tree at `/home/user/sre-monitor-src` (create this directory).
   - Change into the source directory and run `cargo build --release`.
   - Copy the resulting compiled binary to `/home/user/bin/sre-monitor` (create the `/home/user/bin` directory).

3. **The Rust Uptime Monitor:**
   Create a local Git repository in `/home/user/workspace/monitor_code` and initialize a new Rust executable project.
   Write a Rust program that:
   - Reads an environment variable `MONITOR_URL`.
   - Makes a synchronous HTTP GET request to that URL (you may use `ureq` or `reqwest` in blocking mode).
   - If the request is successful (HTTP 200), it appends the exact string "STATUS: UP" to the file `/home/user/mnt/logs/uptime.log`.
   - If the request fails or returns a non-200 status, it appends "STATUS: DOWN" to the same file.
   Commit this code to your local repository and push it to the `master` branch of the bare repository at `/home/user/sre-monitor.git` to trigger the deployment hook.

4. **Execution Wrapper:**
   Write a shell script at `/home/user/run_monitor.sh` that does the following:
   - Executes `/home/user/mount_logs.sh` to mount the log directory.
   - Starts a background Python HTTP server on `127.0.0.1:8080` serving the directory `/home/user` (e.g., `python3 -m http.server 8080 --bind 127.0.0.1 &`).
   - Sleeps for 2 seconds to ensure the server is up.
   - Executes the deployed Rust binary `/home/user/bin/sre-monitor` with `MONITOR_URL=http://127.0.0.1:8080/`.
   - Kills the background Python server.
   - Unmounts the log directory using `fusermount -u /home/user/mnt/logs`.

Once you have written all the components, run `/home/user/run_monitor.sh` once so that the `uptime.log` file is populated and synced back to `/home/user/logs_pool/uptime.log`.