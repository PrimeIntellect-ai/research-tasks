You are an edge computing engineer deploying services to an IoT gateway. You need to set up a Git-based automated deployment pipeline that compiles and runs a C-based monitoring daemon. 

Your objective is to create a bare Git repository that acts as the deployment server, a post-receive hook that manages the lifecycle of the daemon, and the daemon itself written in C.

Perform the following steps:

1. Create a bare Git repository at `/home/user/edge-update.git`.

2. Create a deployment directory at `/home/user/deployed`.

3. Write a Git `post-receive` hook in the bare repository (`/home/user/edge-update.git/hooks/post-receive`). The hook MUST do the following when a push occurs:
   - Read the standard input which Git provides to `post-receive` hooks (format: `<oldrev> <newrev> <refname>`).
   - Checkout the pushed code to the work tree `/home/user/deployed`.
   - Compile the file `device_monitor.c` into an executable named `monitor` in the `/home/user/deployed` directory.
   - Gracefully terminate the old daemon if it is running: check for the existence of `/home/user/monitor.pid`. If it exists, read the PID, send a `SIGTERM` to that process, and ensure it is dead.
   - Start the newly compiled `monitor` executable in the background.
   - Use text processing (e.g., `awk`) to extract the `<newrev>` commit hash from the hook's standard input. Append exactly the string `DEPLOYED: <newrev>` to the file `/home/user/deploy.log`.

4. Create a regular Git repository at `/home/user/source-repo`. Inside it, write a C program named `device_monitor.c` with the following requirements:
   - Upon starting, it must write its own Process ID (PID) to `/home/user/monitor.pid`.
   - It must open a TCP socket and listen for incoming connections on `127.0.0.1` port `9090`.
   - When a client connects and sends the exact string `"PING\n"`, it must respond with `"PONG\n"`, close that specific client connection, and continue listening for new connections.

5. Commit your `device_monitor.c` file to the `main` branch in `/home/user/source-repo`.

6. Add the bare repository `/home/user/edge-update.git` as a remote named `origin` to `/home/user/source-repo`, and `git push origin main` to trigger the deployment pipeline.

Ensure that by the end of your run, the push has succeeded, the daemon is running in the background, `/home/user/deploy.log` contains the deployment record, and the daemon correctly answers to TCP pings on port 9090.