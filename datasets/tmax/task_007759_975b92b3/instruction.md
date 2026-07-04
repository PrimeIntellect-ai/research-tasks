You are a container specialist managing a set of internal microservices for a legacy mailing list system. You are migrating this system to be managed by user-level systemd units, but you are experiencing startup race conditions where the task automation script fires before the mailing daemon is ready.

Your task is to write the daemon, the automation script, and the proper systemd configuration to eliminate these startup errors.

**Phase 1: The Mailing Daemon (C++)**
Write a C++ program at `/home/user/micro_mailer.cpp` and compile it to `/home/user/micro_mailer`.
The daemon must:
1. Listen for incoming TCP connections on `127.0.0.1` port `9922`.
2. When a client connects, immediately send the string `READY_FOR_COMMAND\n`.
3. Read the client's response. If the client sends exactly `DISPATCH_DIGEST` (ignoring trailing newlines/carriage returns), the daemon must append the string `DIGEST_DISPATCHED_TO_LIST` (followed by a newline) to the file `/home/user/digest.log`.
4. Close the connection and continue listening for the next client.

**Phase 2: The Automation Script (Expect)**
Write an Expect script at `/home/user/auto_dispatch.exp`.
The script must:
1. Spawn a connection to the daemon using `nc 127.0.0.1 9922`.
2. Wait to receive the `READY_FOR_COMMAND` prompt.
3. Send the string `DISPATCH_DIGEST` followed by a carriage return or newline.
4. Exit cleanly.

**Phase 3: Service Supervision & Configuration (systemd)**
Create two user-level systemd unit files in the directory `/home/user/.config/systemd/user/` (you will need to create this directory structure).

1. `mailer_daemon.service`:
   - Runs the executable `/home/user/micro_mailer`.
   - Must be configured with a process supervision restart policy so that it always restarts if it crashes (use `Restart=always`).

2. `dispatch_job.service`:
   - Runs the automation script using `/usr/bin/expect /home/user/auto_dispatch.exp`.
   - Must be of `Type=oneshot`.
   - **Crucial Fix:** This service must be explicitly configured to start *strictly after* `mailer_daemon.service` and must declare a strong dependency on it so that systemd knows it requires the daemon to function. Use the correct `[Unit]` properties to define this relationship.

You do not need to start or enable the systemd services using `systemctl` (as the container environment may not run a full systemd user session during this task). Ensure your code compiles, your Expect script works against the daemon, and your systemd unit files are correctly written.