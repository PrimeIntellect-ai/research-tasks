You are a monitoring specialist tasked with resolving an issue where our NGINX proxy returns 502 Bad Gateway errors due to an unstable upstream custom daemon. You need to create an alert filter and a supervision script to keep the system running and properly monitored.

Your objectives:

1. **Alert Filter (C Programming)**: 
   We receive a continuous stream of logs on standard input. Attackers frequently try to trigger false alerts by spoofing error messages in their User-Agent strings, which appear in our combined access logs.
   Write a C program at `/home/user/alert_filter.c` and compile it to `/home/user/alert_filter`. This program must read line-by-line from `stdin` and print to `stdout` *only* the genuine NGINX error log lines that indicate a failure to connect to our upstream socket. 
   A genuine error log strictly contains: `[error]` and the substring `connect() to unix:/app/run/upstream.sock failed (111: Connection refused)`.
   It must completely ignore and suppress lines that are `[info]`, `[warn]`, access logs (where the error might be injected in the URL or headers), or other unrelated errors. 

2. **Process Supervision (Bash)**:
   We have a pre-compiled, stripped binary at `/app/upstream_daemon` which serves as our upstream application. Unfortunately, it crashes sporadically. 
   Write a bash script at `/home/user/supervise.sh` that does the following in an infinite loop:
   - Starts `/app/upstream_daemon` in the foreground.
   - If it crashes or exits, restarts it immediately.
   (The script itself will be run in the background by our CI system).

3. **Directory and Link Management**:
   Inside `/home/user/supervise.sh`, before starting the daemon loop, ensure the directory `/app/run/` exists. Then, create a symbolic link at `/home/user/active_socket` that points to `/app/run/upstream.sock` so our local debuggers can easily access it.

4. **SSH Tunneling**:
   Also inside `/home/user/supervise.sh`, before the loop, establish a background SSH tunnel that forwards your local port `8080` to port `80` on `localhost`. Use the command `ssh -N -f -L 8080:localhost:80 localhost` (assume SSH keys are already set up for passwordless login to localhost).

Make sure your C program is robust against long lines and correctly handles EOF. Your bash script should use standard shell built-ins and coreutils.