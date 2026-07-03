You are a network engineer tasked with troubleshooting and automating a custom deployment pipeline for a reverse proxy. 

Your organization uses a proprietary administration tool, provided as a stripped binary at `/app/lb_admin`. You need to set up an automated configuration sync pipeline and write a custom reverse proxy in Rust.

Here are your objectives:

1. **Git Configuration Sync**:
   - Initialize a bare Git repository at `/home/user/lb_sync.git`.
   - Create a `post-receive` hook in this repository that extracts the pushed files into `/home/user/lb_config/`.
   - After checking out the files, the hook must execute an expect script at `/home/user/reload.exp`.

2. **Expect Scripting**:
   - Write an expect script at `/home/user/reload.exp` that automates interacting with `/app/lb_admin`.
   - You can manually run `/app/lb_admin` to reverse-engineer its prompts. The default credentials are Username: `admin` and Password: `secret123`.
   - The script must log in, issue the command to reload the configuration, and then cleanly quit the CLI. 
   - A successful reload via the CLI will automatically update a timestamp in `/home/user/lb_config/reload_flag`.

3. **Rust Reverse Proxy**:
   - Create a Rust project in `/home/user/rust_proxy`.
   - The program must compile to a binary named `rust_proxy` (run `cargo build --release`).
   - The proxy must listen for incoming TCP connections on `127.0.0.1:8080`.
   - For each connection, read the first line (up to `\n`). The line will be formatted as `ROUTE <target>`.
   - The proxy must look up `<target>` in `/home/user/lb_config/routes.json` (which will contain a flat key-value mapping of targets to local port numbers, e.g., `{"app1": 8081, "app2": 8082}`).
   - If the target is found, connect to `127.0.0.1:<port>`, and bi-directionally forward all subsequent traffic between the client and the backend until the connection is closed.
   - If the target is not found or the first line is malformed, close the connection immediately.
   - To achieve high performance, your proxy should NOT parse the `routes.json` file on every single connection. It should cache the configuration and only reload it when the modification time of `/home/user/lb_config/reload_flag` changes.

Ensure your Rust proxy handles concurrent connections gracefully. The automated test will push a new configuration to your Git repository, verify that the `reload_flag` was updated by your expect script via the hook, and then blast your proxy with traffic to calculate the successful routing rate.