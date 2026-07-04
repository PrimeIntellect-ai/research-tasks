You are a monitoring specialist setting up an alerting pipeline for a staged deployment of our new application infrastructure.

Our system currently logs web proxy traffic and email gateway metrics. You need to configure a log detector, an alert mailer, a local alert dashboard, and a staged deployment script that wires these components together.

You have the following objectives:

1. **Fix the Alert Mailer (Vendored Package)**
We use a third-party Rust package, `alert-mailer` (version 1.0.0), located at `/app/alert-mailer-1.0.0`. 
Currently, it fails to send alerts in our non-root container environment. It was designed to use standard ports, but we must use unprivileged ports. Inspect the package, find the configuration flaw preventing it from connecting to a local SMTP server on port 1025, fix the source code or build configuration, and compile it. The binary should be successfully buildable via `cargo build --release`.

2. **Create the Log Anomaly Detector**
Write a Rust program from scratch in `/home/user/detector/`.
This program must act as a filter/classifier for log lines. 
- It must accept a single command-line argument: the path to a log file.
- It must read the log file line by line.
- If a line contains malicious signatures (specifically: `<script>`, `UNION SELECT`, `DROP TABLE`, or `/etc/passwd`), it must output `[ALERT] <original_line>`.
- If a line is benign, it must output `[OK] <original_line>`.
- The program must write its results to standard output. 

3. **Staged Deployment & Service Setup**
Write a bash script at `/home/user/deploy.sh` that performs the following actions:
- **Mount Configuration**: Create a directory `/home/user/live_logs`. Use `bindfs` (which is installed) to mount `/home/user/raw_logs` to `/home/user/live_logs` in read-only mode (`-o ro`).
- **Email Server**: Start a local debugging SMTP server in the background bound to `localhost:1025` (you can use `python3 -m smtpd -c DebuggingServer -n localhost:1025` or the `aiosmtpd` equivalent).
- **Web Dashboard & TLS**: Create a directory `/home/user/dashboard`. Create a simple `index.html` inside it that says "Alerts Dashboard". Start a local Python HTTPS server in the background on port `8443` serving the `/home/user/dashboard` directory. Use the provided TLS certificates at `/home/user/certs/cert.pem` and `/home/user/certs/key.pem` to secure it.
- **Deployment**: Compile your Rust detector in release mode and copy the compiled binary to `/home/user/bin/detector`.

Make sure `/home/user/deploy.sh` is executable. You do not need to run the `deploy.sh` script to completion if it blocks, but ensure all commands are correctly formatted so our automated test suite can execute it.