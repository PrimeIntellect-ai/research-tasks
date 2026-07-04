You are a container specialist tasked with deploying a locally-hosted, fault-tolerant "Mail Router" microservice system. Because this runs in a user-space container without systemd and without root privileges, you must set up process supervision, a reverse proxy load balancer, and write the backend microservice yourself in C++.

Here are the requirements:

1. **The Backend Microservice (C++)**:
   Write a C++ program at `/home/user/mail_router/router.cpp` and compile it to `/home/user/mail_router/router`. 
   The program must accept a single command-line argument: a port number to listen on.
   It should create a TCP server socket listening on `127.0.0.1` at the specified port.
   For each accepted connection, it must read exactly two lines (terminated by `\n`):
   - Line 1: A command and an email address, formatted as `ROUTE <email_address>` (e.g., `ROUTE admin@local.test`). Alternatively, it can be the single word `CRASH`.
   - Line 2: The message payload (a string).
   
   Behavior:
   - If Line 1 is `CRASH`, the service must immediately reply with `BYE\n` to the socket, close the connection, and exit the process with status code `1` (simulating a fatal failure).
   - If Line 1 is `ROUTE <email_address>`, it must append the message payload (Line 2) followed by a newline `\n` to the file `/home/user/mail_spool/<email_address>.log`. Then, it must reply to the socket with `DELIVERED\n` and close the connection.
   - The server must run continuously, handling one connection after another, until killed.

2. **Process Supervision**:
   Create a supervisord configuration file at `/home/user/mail_router/supervisord.conf`.
   It must manage three instances of the `router` microservice, listening on ports `9001`, `9002`, and `9003`.
   You must configure supervisord so that these processes are automatically restarted if they crash (e.g., `autorestart=true`).
   Run the supervisord process in the background.

3. **Load Balancer**:
   Configure `haproxy` to act as a TCP reverse proxy and load balancer.
   Create the configuration file at `/home/user/mail_router/haproxy.cfg`.
   The load balancer must:
   - Run as the current user, without requiring root privileges.
   - Listen on `127.0.0.1:8080`.
   - Distribute incoming TCP connections using a `roundrobin` algorithm across the three backend instances (`127.0.0.1:9001`, `127.0.0.1:9002`, `127.0.0.1:9003`).
   - Run `haproxy` in the background using this configuration.

Before you consider the task complete, ensure that:
- `supervisord` and `haproxy` are running in the background.
- The `/home/user/mail_spool/` directory exists.
- A client can successfully connect to port 8080, route messages, and even if a `CRASH` payload is sent (crashing one backend), subsequent connections to 8080 are successfully routed to the surviving/restarted backends.