You are a capacity planner for a cloud provider. You need to build an automated verification and provisioning pipeline to analyze and enforce resource usage constraints. You have been provided with a proprietary, stripped binary at `/app/capacity_oracle` which validates if a requested VM configuration falls within our allowed capacity constraints.

Your objective is to implement a Rust-based capacity server, configure a Git-based workflow, and manage QEMU instances for provisioning. Since you do not have root access, all services must be run under your user account.

Complete the following steps:

1. **Bare Git Repository & Hook:**
   - Initialize a bare Git repository at `/home/user/vm-specs.git`.
   - Create a `pre-receive` git hook in this repository. 
   - When a user pushes commits, the hook must inspect all `.json` files that are being added or modified in the push.
   - For each `.json` file, the hook must send its contents to your capacity server's `/verify` endpoint (described below) via a `POST` request. If the server responds with a body containing the exact string `"REJECT"`, the hook must abort the push. Otherwise, it should allow it.

2. **Rust Capacity Server:**
   - Create a new Rust project at `/home/user/cap-server`.
   - Implement an HTTP server (you may use `hyper`, `axum`, or standard library `std::net::TcpListener`) that listens on `127.0.0.1:8080`.
   - Implement a `POST /verify` endpoint. It will receive a JSON payload of the form `{"ram_mb": <integer>, "cpu_cores": <integer>}`.
   - The endpoint must execute the binary `/app/capacity_oracle <ram_mb> <cpu_cores>`. It should return an HTTP 200 OK response where the body is the exact standard output of the oracle binary.
   - Implement a `POST /allocate` endpoint. It receives the same JSON payload. First, it should check the oracle. If the oracle outputs `"OK"`, it must spawn a detached QEMU instance representing the allocation. Use the following command format: 
     `qemu-system-x86_64 -m <ram_mb> -smp <cpu_cores> -vnc 127.0.0.1:1 -daemonize`
     If the oracle outputs `"REJECT"`, it should return an HTTP 400 Bad Request and not start QEMU.

3. **Service Lifecycle Management:**
   - Manage the Rust capacity server using a user-level systemd service.
   - Create a systemd unit file so that running `systemctl --user start cap-server` builds (if necessary) and runs your Rust binary in the background.
   - Ensure the service is running and listening on `127.0.0.1:8080` by the end of your execution.

Ensure your code handles basic errors (like malformed JSON) gracefully. Do not modify the `/app/capacity_oracle` binary.