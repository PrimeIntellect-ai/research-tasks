You are an expert system administrator and monitoring specialist. We need to deploy a custom, high-performance monitoring stack that processes logs from a local dummy web service, generates alerts, and commits those alerts to a local Git repository for auditing.

Your task consists of the following steps:

1. **Service Configuration (Process Supervision & User Accounts):**
   - We have three services located in `/home/user/app/`:
     1. `web_server.py`: A simulated web server writing logs to `/home/user/app/logs/access.log`.
     2. `git_auditor.py`: A local server listening on port 8080 that accepts POST requests with alert data and commits them to a bare Git repository at `/home/user/git/alerts.git`.
     3. `rust_monitor`: A Rust project in `/home/user/app/rust_monitor/` designed to tail the access log, parse it, and send high-severity alerts to the `git_auditor` on port 8080.
   - Configure a user-level `supervisord` instance using a configuration file at `/home/user/app/supervisord.conf` that manages all three processes. Ensure they automatically restart on failure. 

2. **Log Management:**
   - Configure `logrotate` for the `/home/user/app/logs/access.log` file. Write the configuration to `/home/user/app/logrotate.conf`. It should rotate daily, keep 7 backups, compress old logs, and create a new log file with permissions `0644`.

3. **Rust Monitor Optimization (Metric Challenge):**
   - The current Rust implementation in `/home/user/app/rust_monitor/src/main.rs` is extremely slow and naive. It struggles to process the initial backlog of 500,000 log lines.
   - You must refactor `main.rs` to optimize the parsing logic. The parsing step (which extracts 500 errors from the 500k lines) must execute in under **150 milliseconds** on the provided container environment.
   - The final compiled binary must output a benchmark log file at `/home/user/app/metrics.txt` containing only the execution time in milliseconds for the backlog parsing phase (e.g., `124`).

Provide the optimized Rust code, the supervisord config, and the logrotate config. Compile the Rust code in release mode. Ensure all services can successfully start and communicate.