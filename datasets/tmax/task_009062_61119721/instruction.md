You are a cloud architect managing a migration from legacy backend servers to a new infrastructure. To facilitate zero-downtime cutovers, you need to build a custom, lightweight Layer-4 (TCP) load balancer in Rust that includes connection diagnostics and process supervision. 

Since you do not have root access in this environment, you must handle the proxy and its supervision entirely in user space.

Your task is to implement the following system:

1. **Rust TCP Load Balancer (`/home/user/tcp_lb`)**:
   - Create a new Rust Cargo project at `/home/user/tcp_lb`.
   - The program must act as a Layer-4 TCP reverse proxy listening on `127.0.0.1:9000`.
   - On startup, it should read a configuration file located at `/home/user/backends.txt`. This file will contain a list of backend addresses (one per line, e.g., `127.0.0.1:9001`).
   - For every incoming connection on port `9000`, the proxy should pick a backend from the list using strict **Round-Robin** scheduling (the first connection goes to the first backend, the second to the second, etc., wrapping around).
   - The proxy must attempt to establish a TCP connection to the chosen backend. 
   - Once connected, it should bidirectionally copy data between the incoming client connection and the backend connection until either side closes.

2. **Connectivity Diagnostics**:
   - If the proxy fails to establish a TCP connection to the selected backend (e.g., connection refused), it must immediately append a line to `/home/user/diagnostics.log` in this exact format:
     `FAIL: <backend_address>` (e.g., `FAIL: 127.0.0.1:9002`)
   - After a failure, it must immediately attempt to connect to the *next* backend in the round-robin sequence to serve the current client connection. It should continue trying subsequent backends until one succeeds or all have been tried.

3. **Process Supervision (`/home/user/supervisor.sh`)**:
   - Write a bash script at `/home/user/supervisor.sh` that acts as a process supervisor for your Rust proxy.
   - The script must change directory to `/home/user/tcp_lb` and execute the proxy (`cargo run --release`).
   - If the proxy process exits for any reason, the supervisor script must automatically restart it.
   - Make sure `/home/user/supervisor.sh` is executable (`chmod +x`).

**Constraints & Assumptions:**
- Do not use complex third-party proxy frameworks; standard library `std::net`, `std::thread`, or basic asynchronous crates (like `tokio` if you prefer, though standard threads are fine) are sufficient.
- The `backends.txt` file will be created by the system before your proxy is evaluated. You can create a mock one to test your code.
- Ensure your Rust code compiles successfully.
- Do not run the supervisor script yourself as a background daemon; the automated test suite will execute `/home/user/supervisor.sh` to start and evaluate your system.