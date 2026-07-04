You are an edge computing engineer responsible for deploying monitoring and backup agents to remote IoT devices with limited connectivity. Because these devices lack full mail servers and run minimal operating systems, you need to build a custom, self-contained health monitor and backup utility using Rust, deployed via a shell script.

Your objective is to create a complete deployment pipeline that sets up directories, compiles a Rust monitoring utility, and executes it to secure device data and trigger offline alerts.

Please complete the following tasks:

1. Create a bash script at `/home/user/deploy.sh`. This script must:
   - Create the directories `/home/user/backups` and `/home/user/smtp_spool`.
   - Initialize a new Rust binary project at `/home/user/edge_agent` (if it doesn't already exist).
   - Build the Rust project in release mode.
   - Execute the compiled binary.
   - Make sure `/home/user/deploy.sh` is executable (`chmod +x`).

2. Write the Rust program for the `edge_agent` (located at `/home/user/edge_agent/src/main.rs`). The program must perform two main operations when run:

   **A. Telemetry Backup:**
   - The IoT device writes sensor data to `/home/user/telemetry_data`.
   - The Rust program must read all files in `/home/user/telemetry_data` and create a compressed tarball (`.tar.gz`) of its contents.
   - Save the tarball exactly to `/home/user/backups/telemetry_latest.tar.gz`. Note: Use the standard `tar` CLI command via Rust's `std::process::Command` to perform this, or use a crate. Using `Command::new("tar").arg("-czf")...` is highly recommended for simplicity. The archive must contain the files from `telemetry_data` (either absolute paths or relative, as long as extracting it yields the files).

   **B. Health Check & Email Alerting:**
   - The device's hardware watchdog writes status logs to `/home/user/device_health.log`.
   - The Rust program must read this file.
   - If (and only if) the file contains the exact string `CRITICAL`, the program must generate an email file at `/home/user/smtp_spool/alert.eml`.
   - The generated `.eml` file must strictly adhere to the following format (RFC 2822 subset) so a spooler daemon can pick it up:
     ```
     From: edge-daemon@iot.local
     To: noc@edge-corp.local
     Subject: [ALERT] Edge Device Failure

     Hardware watchdog reported a CRITICAL error.
     ```
     (Ensure there is exactly one empty line between the headers and the body).

3. Finally, execute your `/home/user/deploy.sh` script to verify everything works. The environment already has a populated `/home/user/telemetry_data` directory and a `/home/user/device_health.log` file.