You are tasked with porting a legacy analytics tool into a minimal containerized service structure. You need to wrap a proprietary binary with an HTTP interface, repair a broken auditing component, set up a reverse proxy, and reconcile historical logs.

Work entirely within `/home/user/workspace`. Do not use `sudo` or require root access.

**1. The Analytics Wrapper (Bash State Machine & Parser)**
We have a proprietary, stripped executable located at `/app/evaluator`. It accepts a single math/logic expression on standard input, evaluates it, and prints the result to standard output.
You must write a Bash script `/home/user/workspace/api.sh` that acts as an HTTP server listening on TCP port `9001`. 
- It must parse incoming HTTP POST requests. You will need to implement a basic state machine in Bash to read HTTP headers, extract the `Content-Length`, read the exact body payload, and pass it to `/app/evaluator`.
- It must return a valid `HTTP/1.1 200 OK` response with the correct `Content-Length` and the exact output of `/app/evaluator` as the response body.
- Note: Do not use Python or other high-level languages for the server; use Bash and standard utilities like `nc`, `socat`, `gawk`, or `sed`.

**2. The Audit Logger (C Program & Makefile Repair)**
In `/home/user/workspace/audit/`, there is a C source file `audit.c` and a `Makefile`. This daemon receives log events over raw TCP.
- The `Makefile` is broken and fails to compile the `audit` binary. Fix the `Makefile` and compile the program.
- Run the compiled `audit` binary in the background. It will bind to TCP port `9002`.
- Update your `api.sh` so that immediately after sending the response to the client, it sends the raw body payload (the expression evaluated) via a raw TCP connection to `127.0.0.1:9002`.

**3. The Reverse Proxy**
Create an Nginx configuration file at `/home/user/workspace/nginx.conf`.
- Configure Nginx to run unprivileged (use `/tmp/` for pids, client bodies, and logs).
- It must listen on TCP port `8080`.
- It must reverse proxy all requests sent to the endpoint `/api/v1/check` to your Bash server at `127.0.0.1:9001`.

**4. Log Reconciliation (Sorting, Merging, Diffing)**
We have two historical log files: `/app/logs/server_a.log` and `/app/logs/server_b.log`.
Write a script `/home/user/workspace/reconcile.sh` that:
- Sorts both files alphabetically.
- Merges them into a single deduplicated list.
- Performs a diff between this merged list and `/app/logs/baseline.log`.
- Saves the unified diff to `/home/user/workspace/diff.out`.

Ensure all services (Nginx, the Audit daemon, and `api.sh`) are running in the background before you finish.