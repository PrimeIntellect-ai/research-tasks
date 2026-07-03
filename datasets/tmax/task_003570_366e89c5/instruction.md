You are a container specialist managing a new microservice architecture. A custom gateway daemon, currently provided as a vendored source package, is failing to build and run correctly. Your goal is to fix the package, configure the environment, and establish secure access to it.

Here are your tasks:

1. **Fix and Build the Vendored Package:**
   You will find the source code for the gateway daemon extracted at `/app/microservice-gateway-1.2`.
   - The `Makefile` has a syntax error or missing directive preventing it from linking correctly.
   - The C source file (`gateway.c`) has a typo where it attempts to read the management port from an environment variable. It currently reads `GETWAY_PORT` instead of the expected `GATEWAY_PORT`.
   - Fix both issues, compile the project by running `make` in that directory, and ensure the resulting `gateway_daemon` executable is built.

2. **Environment Configuration:**
   Create an idempotent shell script at `/home/user/setup_env.sh` that adds the following environment variables to `/home/user/.bashrc` (ensure it does not add duplicate entries if run multiple times):
   - `GATEWAY_PORT=9000`
   - `HTTP_PORT=9001`
   - `GATEWAY_TOKEN=secure-micro-token`
   Source your `.bashrc` or export these in your current session, then start the `gateway_daemon` in the background.

3. **Interactive Automation (Expect):**
   The gateway daemon's management interface listens on raw TCP on `GATEWAY_PORT` (9000). It requires an interactive login before it activates the HTTP listener on `HTTP_PORT`.
   - Inspect `gateway.c` to find the hardcoded admin username and password.
   - Write an Expect script at `/home/user/enable_http.exp` that connects to `127.0.0.1:9000` (e.g., using `nc` or `telnet`), waits for the `Username:` and `Password:` prompts, submits the credentials, and then sends the command `ENABLE HTTP`.
   - Run this script to activate the HTTP endpoint.

4. **SSH Port Forwarding:**
   Direct access to the HTTP port (9001) is prohibited by external firewall rules in our production setup. We simulate this by requiring an SSH tunnel.
   - Generate an SSH keypair for the `user` account and authorize it in `/home/user/.ssh/authorized_keys` so you can SSH into `localhost` without a password.
   - Establish a background SSH port forwarding session that listens on local port `8080` and forwards traffic to `127.0.0.1:9001`.

Once complete, the automated verifier will attempt to send an HTTP GET request to `127.0.0.1:8080` with the header `Authorization: Bearer secure-micro-token` to verify the microservice gateway is active and fully functional.