You are a cloud architect migrating a legacy backend service to a modern microservices architecture. To ensure zero downtime, you are setting up a Rust-based intelligent routing proxy that fronts the legacy system, which currently runs inside an emulated QEMU virtual machine.

Your objective is to complete the Rust proxy, configure the environment, and create an integration script to bring all the services up correctly.

**Here is your task:**

1. **Legacy VM Setup:**
   There is a script located at `/app/start_legacy_vm.sh`. This script boots a lightweight QEMU virtual machine running the legacy service. When started, the legacy service binds to `127.0.0.1:9090` on the host system. It accepts raw TCP connections and responds with legacy data.

2. **Rust Router Implementation:**
   You have been provided a skeleton Rust application in `/app/router_template`. Copy this directory to `/home/user/router`.
   Modify the Rust code (e.g., `src/main.rs`) to implement the following multi-protocol behavior:
   * **HTTP Service:** Listen on `127.0.0.1:8000`. When a `GET /info` request is received, it must respond with a 200 OK and a JSON payload containing the configured timezone and the target IP of the legacy VM. The JSON must exactly match this format:
     `{"tz": "<value_of_TZ_env_var>", "legacy_target": "127.0.0.1:9090"}`
   * **TCP Proxy Service:** Listen on `127.0.0.1:8001` for raw TCP connections. When a client connects, the proxy must read the first line (up to `\n`). 
     * If the first line is exactly `AUTH: v2migrate\n`, the proxy must strip this authentication line and establish a bidirectional proxy (forwarding all subsequent bytes back and forth) between the client and the legacy VM at `127.0.0.1:9090`.
     * If the authentication line is incorrect or missing, the proxy should immediately drop the connection.

3. **Environment & Automation:**
   Write a bash script at `/home/user/run_stack.sh` that does the following:
   * Sets the `TZ` environment variable to `Asia/Tokyo`.
   * Sets the `LANG` environment variable to `C.UTF-8`.
   * Starts the legacy VM via `/app/start_legacy_vm.sh` in the background.
   * Compiles (if not already compiled) and starts the Rust router in the background.
   * Make sure both processes remain running when the script finishes.

Build the Rust project and verify it compiles. Once you are confident, run your `/home/user/run_stack.sh` script to bring up the environment.

Ensure your code is robust, handles basic network errors gracefully without crashing, and relies entirely on standard CLI tools and standard Rust libraries (or libraries pre-included in the provided `Cargo.toml`). Do not run the applications as root.