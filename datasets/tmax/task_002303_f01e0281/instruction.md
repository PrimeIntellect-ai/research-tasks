You are a monitoring specialist tasked with fixing a broken microservice setup and deploying a high-performance alert parser.

The application resides in `/app/`. A startup script `/app/start_services.sh` launches three simulated services:
- **DB Service**: listens on `127.0.0.1:9001`
- **Backend Service**: listens on `127.0.0.1:9002`
- **Frontend Service**: listens on `127.0.0.1:9003`

However, there is a network misconfiguration. The Frontend expects the Backend to be on port `8002`, and the Backend expects the DB to be on port `8001`. 
Your tasks are as follows:

1. **Fix Communications**: Use SSH local port forwarding to map port `8002` to `9002` and port `8001` to `9001` on localhost. You may need to generate an SSH key and add it to your `~/.ssh/authorized_keys` to allow passwordless SSH to `localhost` for the `user` account. Ensure the tunnels are running in the background. Once correctly forwarded, sending a `GET /` to `http://127.0.0.1:9003` should successfully chain through all three services and return `HTTP 200 OK`.

2. **Storage Management**: Create a directory `/app/logs`. Mount a `tmpfs` to `/app/logs` with a maximum size of `50M` (You can use a user-space mount if you lack root, or if you have sudo, use it just for the mount. Assume you have `sudo` privileges for mounting).

3. **High-Performance Log Parser (C)**:
   The Backend service writes traffic logs to a file. A historical snapshot is located at `/app/historical.log`.
   The log lines look like this: `[2023-10-12T10:00:00] txid=A1B2C3 status=200 time=45ms`
   Write a C program that reads a log file specified by the first command-line argument. It must extract the `txid` of any request where the `time` value is **strictly greater than 500ms**, and print those `txid`s (one per line) to standard output. 
   Save your source code as `/home/user/workspace/alert_parser.c`.
   
4. **Git Automation**:
   Initialize a bare Git repository at `/home/user/monitor.git`.
   Clone it to `/home/user/workspace`. 
   Create a `post-receive` hook in the bare repository that automatically compiles the C program using `gcc -O3` and saves the executable to `/app/bin/alert_parser` whenever new code is pushed.
   Commit and push your C code to trigger the hook.

5. **Final Output**: Run your compiled program against `/app/historical.log` and redirect the output to `/app/logs/alerts.txt`.

**Constraints & Verification**:
Your C program will be evaluated against a massive hidden log file using a **metric threshold**. It must correctly identify all slow transactions with 100% accuracy, and its execution time must be less than `0.2` seconds for a 1,000,000-line log file.