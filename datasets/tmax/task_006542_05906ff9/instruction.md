You are an infrastructure engineer tasked with building a custom health-checking proxy manager. You need to write a Rust-based health check utility and a bash script to manage a port-forwarding proxy based on the health status.

Step 1: Create the Health Checker (Rust)
Create a new Cargo project at `/home/user/health_checker`.
Modify `src/main.rs` to create a CLI tool that takes a single argument: a port number.
The tool must:
1. Connect via TCP to `127.0.0.1:<port>`.
2. Send the string `PING\n`.
3. Read the response. 
4. If the response is exactly `PONG\n`, print `HEALTHY` to standard output and exit with status code 0.
5. If the connection fails, or the response is anything else, print `UNHEALTHY` to standard output and exit with status code 1.
*(Make sure to handle connection timeouts gracefully, e.g., 2 seconds, to prevent hanging).*

Step 2: Create the Proxy Manager (Bash)
Create an executable bash script at `/home/user/manager.sh`.
When executed, this script must do the following in order:
1. Compile the Rust project in `/home/user/health_checker` using `cargo build --release`.
2. Start a TCP port forwarder in the background using `socat`. It should listen on `127.0.0.1:8080` and forward to `127.0.0.1:9090` (`socat TCP-LISTEN:8080,fork,bind=127.0.0.1 TCP:127.0.0.1:9090`).
3. Save the PID of this background `socat` process to `/home/user/proxy.pid`.
4. Enter an infinite loop that runs every 1 second:
   a. Execute the compiled Rust health checker against port `9090`.
   b. Append the result to `/home/user/monitoring.log` in the format: `<UNIX_EPOCH_TIMESTAMP> <HEALTHY|UNHEALTHY>`. (e.g., `1690000000 HEALTHY`).
   c. If the health checker exits with a non-zero status (fails), immediately kill the `socat` process using the PID stored in `/home/user/proxy.pid`, log the failure to `monitoring.log`, and `exit 1` from the bash script.

Ensure both the Cargo project is properly initialized and the `manager.sh` script is executable (`chmod +x`). Do not start the `manager.sh` script; the automated verification will run it.