You are an edge computing engineer configuring a newly provisioned IoT gateway device. Your goal is to deploy the `edge-proxy` telemetry daemon, which is critical for relaying metrics and control commands to our central servers. 

Currently, the source code for the proxy is shipped on the device, but it has not been configured, built, or started, and a recent upstream commit introduced a bug that causes it to silently drop authenticated control commands (similar to an SSH misconfiguration that silently rejects valid keys).

Please complete the following deployment steps:

1. **Directory & Link Setup**: 
   The proxy source code is vendored at `/app/edge-proxy-1.2.0`. Create a symbolic link at `/app/current` pointing to this directory. The daemon will expect its configuration file to exist at `/app/etc/edge-proxy.toml`. You will need to create the `/app/etc` directory and write a configuration file there (format detailed below). Also, create a directory for logs at `/app/var/log/`.

2. **Configuration File**:
   Create `/app/etc/edge-proxy.toml` with the following content:
   ```toml
   [server]
   http_port = 9090
   tcp_port = 9091
   
   [auth]
   control_token = "edge-init-token-8842"
   ```

3. **Code Fix**:
   Inspect the Rust source code in `/app/current`. There is a bug in the authentication logic (`src/auth.rs` or `src/main.rs`) that causes the daemon to silently reject the valid `control_token` provided in the configuration. Identify the perturbation and fix it so that valid tokens are accepted. Once fixed, build the package using `cargo build --release`.

4. **Service Lifecycle & Environment (Locale/Timezone)**:
   We cannot rely on system-wide timezone settings because this gateway might physically move. Instead, configure a user-level systemd service to manage the daemon.
   Create a systemd user service file at `/home/user/.config/systemd/user/edge-proxy.service`. 
   The service must:
   - Execute the compiled binary at `/app/current/target/release/edge-proxy`
   - Set the `TZ` environment variable to `Asia/Tokyo`
   - Set the `LANG` environment variable to `en_US.UTF-8`
   - Pass the configuration file path as an argument if required by the daemon, or ensure it's picked up from `/app/etc/edge-proxy.toml` (the app looks for it at `../etc/edge-proxy.toml` relative to the `/app/current` symlink by default if executed in `/app/current`, but specifically set the working directory of the systemd service to `/app/current`).
   - Write standard output and standard error to `/app/var/log/edge-proxy.log`.

5. **Final Integration**:
   Reload the systemd user daemon, start `edge-proxy.service`, and enable it to start on boot. Ensure both the HTTP health endpoint and the TCP control endpoint are listening and responding correctly.