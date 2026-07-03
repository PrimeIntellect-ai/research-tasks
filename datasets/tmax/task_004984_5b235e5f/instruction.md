You are tasked with setting up a custom, lightweight load-balancer service and its monitoring infrastructure for a set of internal backend applications.

You need to implement the following components entirely in the `/home/user` directory:

1. **The C Load Balancer (`/home/user/lb.c`)**
Write a C program that acts as a simple TCP round-robin load balancer. 
- It must listen on TCP port `8000`.
- It must accept incoming connections and forward the traffic to two backend servers listening on `127.0.0.1:8001` and `127.0.0.1:8002`.
- It must strictly alternate between the two backends for each new incoming connection (Round-Robin: connection 1 goes to 8001, connection 2 goes to 8002, connection 3 to 8001, etc.).
- For each connection, it only needs to handle a single request/response cycle: read up to 1024 bytes from the client, send it to the backend, read up to 1024 bytes from the backend, send it to the client, and then close all sockets for that session.
- Compile this program to an executable named `/home/user/lb`.

2. **The Monitor Script (`/home/user/health.sh`)**
Write a robust Bash script that ensures the load balancer is running.
- It should check if a process is listening on port `8000`.
- If the load balancer is NOT running, the script must:
  a) Append the exact string `[CRASH DETECTED] Restarting LB` to `/home/user/lb.log`.
  b) Start the `/home/user/lb` executable in the background.
- Make sure the script is executable.

3. **Scheduled Task (Cron)**
- Install a user-level crontab that executes `/home/user/health.sh` every minute.

Constraints:
- You do not have root access. Use standard user directories and ports above 1024.
- Use basic C standard libraries (`<stdio.h>`, `<stdlib.h>`, `<string.h>`, `<unistd.h>`, `<sys/socket.h>`, `<netinet/in.h>`, `<arpa/inet.h>`).
- Do not use external load balancing software (like HAProxy or Nginx); you must implement the C program as requested.