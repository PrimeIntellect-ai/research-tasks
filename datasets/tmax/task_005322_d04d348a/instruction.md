You are tasked with fixing a custom "operator" for a simulated CI/CD environment. A previous engineer tried to implement a custom user-space reverse proxy and load balancer in Rust to resolve a network misconfiguration where local services couldn't reach each other. The Rust application is supposed to act as a TCP reverse proxy, but the code is missing, and the deployment script is incomplete.

Your objective is to complete the Rust application and its deployment script.

1. **The Rust Reverse Proxy (`/home/user/lb-operator`)**:
   - We have initialized a Rust project at `/home/user/lb-operator`. 
   - Write the logic in `/home/user/lb-operator/src/main.rs`.
   - The program must read a JSON configuration file located at `/home/user/manifest.json`.
   - The JSON file format is: `{"listen": "127.0.0.1:8888", "backends": ["127.0.0.1:9001", "127.0.0.1:9002"]}`
   - The application must bind a TCP listener to the `listen` address.
   - For every incoming TCP connection, it must pick one of the `backends` (simple round-robin or random selection is acceptable), establish a TCP connection to that backend, and bidirectionally proxy all data between the client and the backend.
   - The standard library `std::net::TcpListener`, `std::net::TcpStream`, and `std::thread` are sufficient. The `serde_json` crate is already added to the `Cargo.toml`.

2. **The Idempotent CI/CD Deployment Script (`/home/user/deploy.sh`)**:
   - Write a bash script at `/home/user/deploy.sh` and make it executable (`chmod +x`).
   - The script must be strictly idempotent. When executed, it should:
     a) Navigate to `/home/user/lb-operator` and compile the Rust project in release mode (`cargo build --release`).
     b) Check if a previous instance of the proxy is running by reading the PID file at `/home/user/proxy.pid`.
     c) If a process with that PID is running, safely terminate it (`kill`) and wait for it to stop.
     d) Start the newly compiled Rust binary in the background.
     e) Save the PID of the newly started background process to `/home/user/proxy.pid`.

Make sure your Rust application properly handles continuous streaming until either the client or backend closes the connection. Ensure your bash script uses standard built-ins and coreutils. You do not have root access, so ensure all bindings use user-space local ports (e.g., 127.0.0.1).