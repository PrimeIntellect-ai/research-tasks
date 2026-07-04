You are an infrastructure engineer automating the provisioning of a lightweight, custom container-like environment. You need to create a "container runtime shim" written in Rust that manages the lifecycle of a mock containerized application, extracts network routing data, and handles post-execution backups.

Your task is to create a Rust project at `/home/user/prov-shim` and write a program that fulfills the following strict requirements.

1. **Project Setup**:
   - Initialize a new Rust binary project at `/home/user/prov-shim`.
   - You may use standard library features. If you need external crates (like `regex` or `nix`), add them to your `Cargo.toml`, but standard library alone is sufficient.

2. **Command Line Interface**:
   The compiled binary must accept exactly three command-line arguments (in this order):
   - `workspace_dir`: The directory path where the mock container will run.
   - `port`: The port number the mock container should listen on.
   - `backup_tar_path`: The file path where the workspace backup should be saved.

3. **Lifecycle Management & Network Profiling**:
   When executed, your Rust program must perform the following sequence of actions:
   - **Step A**: Create the `workspace_dir` directory if it does not already exist.
   - **Step B**: Write a file named `status.txt` inside `workspace_dir` containing exactly the word `RUNNING`.
   - **Step C (Routing Config extraction)**: Read the system's IPv4 routing table from `/proc/net/route`. Find the default route (the line where the `Destination` column is `00000000`). Extract the hex string representing the `Gateway` from that line. Write this exact hex string to a file named `gateway.info` inside `workspace_dir`.
   - **Step D (Process Control)**: Spawn a child process to act as the mock container payload. The command to spawn is: `python3 -m http.server <port> --directory <workspace_dir>`.
   - **Step E (Monitoring)**: Allow the child process to run for exactly 5 seconds. You must pause/sleep your Rust program during this time.
   - **Step F**: After 5 seconds, cleanly terminate the child process (e.g., via SIGTERM or `kill()` method) and wait for it to fully exit.
   - **Step G (Backup Strategy)**: After the child process has terminated, create a gzipped tarball of the entire `workspace_dir` and save it to `backup_tar_path`. You must do this by executing the system `tar` command via Rust's `Command` API (e.g., `tar -czf <backup_tar_path> -C <workspace_dir> .`).

4. **Build**:
   - Once your code is complete, compile the project in release mode so that the executable is available at `/home/user/prov-shim/target/release/prov-shim`.

Ensure all file paths and permissions are managed within the user's home directory (`/home/user/`). Do not hardcode specific test paths in your Rust code; strictly use the command-line arguments provided at runtime.