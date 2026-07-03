You are tasked with setting up a continuous deployment pipeline for a local Rust-based microservice health checker, simulating a container orchestration environment's process supervision and network routing. 

Currently, our team is struggling with network misconfigurations between our microservices. To help monitor this, you must write a Rust service that checks backend connectivity, and a robust deployment pipeline that automatically restarts the service whenever new code is pushed.

Perform the following steps exactly as described:

1. **Rust Microservice (`netmon`)**:
   - Create a new Rust project at `/home/user/src/network_monitor` (the binary should be named `netmon`).
   - Write standard-library-only Rust code (no external crates in `Cargo.toml` besides the defaults) that starts an HTTP server listening on `127.0.0.1:8181`.
   - When it receives any HTTP GET request, it should attempt to open a TCP connection to `127.0.0.1:9090`. 
   - If the connection to `9090` succeeds, it must respond with: `HTTP/1.1 200 OK\r\n\r\nUP`
   - If the connection fails, it must respond with: `HTTP/1.1 503 Service Unavailable\r\n\r\nDOWN`

2. **Git Server & Hook (Task Automation & Process Supervision)**:
   - Initialize a bare git repository at `/home/user/registry.git`.
   - Create a `post-receive` hook at `/home/user/registry.git/hooks/post-receive`. Ensure it is executable.
   - The hook must be a bash script that performs the following idempotent steps:
     a. **Disk Quota Check**: Check the available disk space for `/home/user` using `df -k`. If available space is less than 50000 KB, print an error and exit with code 1.
     b. **Checkout**: Check out the incoming code into `/home/user/deploy` (create the directory if it doesn't exist).
     c. **Build**: Run `cargo build --release` in the deploy directory.
     d. **Supervision/Restart**: Find any running process named `netmon` and terminate it safely.
     e. **Start**: Start the newly built `/home/user/deploy/target/release/netmon` in the background. Redirect both stdout and stderr to `/home/user/netmon.log`.

3. **Deployment**:
   - Initialize a git repository in `/home/user/src/network_monitor`.
   - Commit your Rust code.
   - Add the bare repo as a remote named `deploy` (`/home/user/registry.git`).
   - Push the `master` branch to the `deploy` remote to trigger the build and deployment pipeline.

4. **Network Test & Verification**:
   - Once the hook has successfully run and `netmon` is running in the background, start a dummy backend service on port 9090 (e.g., using `python3 -m http.server 9090 &`).
   - Use `curl -s http://127.0.0.1:8181/` to query your Rust microservice.
   - Save the exact string output of the curl command to `/home/user/final_status.txt`.

Ensure all paths, ports, and output strings exactly match the instructions.