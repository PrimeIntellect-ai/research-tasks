You are an administrator for an internal mock user-management system. Since we do not have root access on this node, you need to build a custom user-space daemon in C to manage the "accounts", an Expect script to interact with its password-protected socket, a bash script to manage its lifecycle, and a cron-like scheduled health check.

Perform the following tasks:

1. **Write the C Daemon:**
   Create a C program at `/home/user/account_daemon.c` and compile it to `/home/user/account_daemon`.
   - The daemon must run in the background (fork itself or just run and wait, but your service script will handle backgrounding). 
   - It must listen on a Unix Domain Socket at `/home/user/account.sock`.
   - When a client connects, the daemon must send the exact string `"PASSWD:\n"`.
   - It should then wait for a response. If the client sends `"adminpass\n"`, the daemon replies with `"AUTH_OK\n"`. If the password is wrong or malformed, it replies with `"DENIED\n"` and closes the connection.
   - After authentication, if the client sends `"PING\n"`, the daemon must reply with `"PONG\n"`. 
   - If the client sends `"QUIT\n"`, the daemon closes the connection.
   - The daemon must gracefully handle multiple sequential connections (it does not need to handle concurrent connections, just one after another).

2. **Write a Service Manager Script:**
   Create a bash script at `/home/user/service.sh` that takes one argument: `start` or `stop`.
   - `start`: Starts the `/home/user/account_daemon` in the background. It must save the process ID (PID) to `/home/user/account_daemon.pid`.
   - `stop`: Reads the PID from `/home/user/account_daemon.pid`, sends a SIGTERM to that process, and deletes the PID file and the socket file (`/home/user/account.sock`).

3. **Write an Expect Script for Health Checking:**
   Create an Expect script at `/home/user/health_check.exp`.
   - This script must spawn a connection to the daemon using `nc -U /home/user/account.sock`.
   - It must wait for the `"PASSWD:"` prompt.
   - It must send the password `"adminpass\n"`.
   - It must wait for `"AUTH_OK"`.
   - It must send `"PING\n"`.
   - It must wait for `"PONG"`.
   - Once it sees `"PONG"`, it should exit with status code `0`. If any of these steps time out or fail, it should exit with a non-zero status code.

4. **Setup a Scheduled Health Log:**
   Write a simple bash script `/home/user/monitor.sh` that calls `/home/user/health_check.exp`. If the expect script exits with 0, it appends `"HEALTHY\n"` to `/home/user/health.log`. If it exits with non-zero, it appends `"UNHEALTHY\n"` to `/home/user/health.log`.

Make sure to leave the daemon RUNNING using your `service.sh` script by the time you finish the task.