You are an infrastructure engineer automating the provisioning of a local node. Your goal is to create a lightweight health-check daemon in Rust and set up its service lifecycle configuration.

Perform the following steps:

1. Create a Rust program at `/home/user/infra_agent.rs` that performs the following health checks:
   - Verifies that the environment variable `USER` is set to exactly `user` (User account validation).
   - Verifies that the directory `/home/user/app_storage` exists (Storage monitoring).
   - Attempts to establish a TCP connection to `127.0.0.1:8888` (Connectivity diagnostics).
   
2. If and only if all three checks succeed, the Rust program must append the exact string `SYSTEM_READY` (followed by a newline) to the file `/home/user/health.log`.

3. Compile the program using `rustc` so that the output binary is located exactly at `/home/user/infra_agent`.

4. Create a systemd user unit file for this daemon at `/home/user/.config/systemd/user/infra_agent.service`. The unit file must:
   - Have a `[Service]` section.
   - Set the executable path to `/home/user/infra_agent`.
   - Configure the service to automatically restart if it fails by setting the restart policy to `always`.

Ensure all directories exist before creating files in them. Do not start the service yourself, as systemd PID 1 is not running in this container environment. Just create the compiled binary and the configuration file.