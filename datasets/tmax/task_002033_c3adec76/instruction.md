You are a monitoring specialist deploying a new Rust-based alerting service. The system currently lacks root access, so you cannot use systemd. Instead, you must set up the necessary filesystem structures and write a custom Bash process supervisor to ensure the service dependencies are met and restart policies are enforced.

There are two components:
1. A metrics collector (already provided at `/home/user/collector.sh`). When run, it takes a few seconds to initialize and eventually creates a readiness file.
2. The alerting daemon source code (provided at `/home/user/alerter.rs`).

Your task:
1. Compile `/home/user/alerter.rs` into an executable named `/home/user/alerter`.
2. The `alerter` binary requires a specific directory structure to store state. Create a directory `/home/user/data/releases/v1`. Then, create a symbolic link at `/home/user/data/active` that points to `/home/user/data/releases/v1`.
3. Create a process supervisor script at `/home/user/supervisor.sh` with the following requirements:
   - It must first start `/home/user/collector.sh` in the background.
   - It must continuously check for the existence of `/home/user/data/ready.flag` (created by the collector). It must *not* start the alerter until this file exists (this mimics a missing `After=` systemd dependency).
   - Once the ready flag exists, it must start `/home/user/alerter` in the background.
   - It must monitor the `alerter` process. If the `alerter` process dies or exits for any reason, the supervisor must immediately restart it.
4. Make `supervisor.sh` executable.
5. Run your `/home/user/supervisor.sh` script in the background.
6. Write the Process ID (PID) of the running `supervisor.sh` script to `/home/user/supervisor.pid`.

Leave the supervisor running. We will test your supervisor by programmatically killing the `alerter` process and verifying that your script successfully restarts it.