You are a system administrator tasked with setting up a lightweight, user-space "push-to-deploy" pipeline. Since you do not have root access, you will use standard user-level tools and high ports.

Perform the following tasks:

1. Create a bare Git repository at `/home/user/deploy.git`.
2. Create a directory for the live application at `/home/user/live`.
3. Write a Git `post-receive` hook in `/home/user/deploy.git/hooks/post-receive`. Ensure it is executable. The hook must perform the following actions every time code is pushed:
   - Check out the latest code into the work tree at `/home/user/live`.
   - Gracefully terminate any currently running Python HTTP server that was started by this hook.
   - Start a new Python HTTP server (`python3 -m http.server 8080`) serving the `/home/user/live` directory in the background.
   - Redirect the HTTP server's standard output and standard error to `/home/user/server.log`.
4. Set up a simple reverse proxy/port forward using `socat`. Run a `socat` process in the background that listens on TCP port `8081` and forwards all connections to `localhost:8080`.
5. Save the Process ID (PID) of the background `socat` process to the file `/home/user/socat.pid`.

Make sure the `socat` process is actively running and the Git hook is ready to be triggered. Do not manually start the Python HTTP server; it must only be started via the `post-receive` hook when code is pushed.