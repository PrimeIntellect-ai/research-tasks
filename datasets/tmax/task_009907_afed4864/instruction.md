You are tasked with diagnosing and fixing a systemd user service that keeps crashing on startup, compiling its underlying Rust application, and verifying its logging pipeline. 

Currently, a custom logging application is managed by systemd user services, but it fails to run.

Here is what you need to do:
1. **Compile the Rust Application:**
   There is a Rust project located at `/home/user/rust-app`. Compile this project in release mode and copy the resulting binary to `/home/user/bin/main-app` (create the `bin` directory if it doesn't exist).

2. **Fix Service Dependencies:**
   The `main-app.service` (located in `/home/user/.config/systemd/user/`) keeps failing on startup because it expects certain filesystem structures and timezone configurations to be created by `init-env.service`. However, the dependencies are not configured.
   Modify `/home/user/.config/systemd/user/main-app.service` to ensure it always starts *after* `init-env.service` and explicitly *requires* it to run.
   Once fixed, reload the user daemon and start `main-app.service`.

3. **Verify Log Generation and Rotation:**
   When running correctly, the service will write to `/home/user/logs/app.log`. 
   We need to ensure log rotation is configured correctly for this user. A configuration file exists at `/home/user/logrotate.conf`.
   Execute a single manual log rotation using this configuration file and a state file located at `/home/user/logrotate.state`. (You may need to force the rotation if the log file is too new).

4. **Reporting:**
   After you have successfully started the service and forced a log rotation, write the output of `systemctl --user status main-app.service` to `/home/user/service_status.txt`.
   Next, list the contents of the `/home/user/logs/` directory and save the output to `/home/user/log_dir_listing.txt`.

Ensure all tasks are done entirely in the user space (do not use `sudo` or root privileges).