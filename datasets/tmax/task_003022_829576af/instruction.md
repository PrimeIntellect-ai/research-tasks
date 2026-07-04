You are an engineer diagnosing why a local Rust service fails to start. The service is located in `/home/user/service_app`. When the previous engineer tried to run it, it crashed on startup.

Your objectives are:
1. Diagnose the issue by examining `/home/user/service_app/config.json` and the Rust source code.
2. Fix the configuration file so the service correctly binds to the local loopback IPv4 address instead of the invalid IP address currently specified.
3. The application attempts to write to a log file upon successful startup, but it assumes the logging directory already exists. Create the necessary logging directory as defined in the configuration file.
4. Compile and run the service using `cargo run`. 
5. Once the service runs successfully, it will append a startup message to its log file. Use text processing tools (like `grep` and `awk`) to extract the secret startup token from the log file. The log line will be in the format: `[INFO] Server started successfully. Token: <TOKEN>`
6. Save only the extracted `<TOKEN>` to a new file at `/home/user/solution.txt`.

Ensure that you do not modify the Rust source code itself (`main.rs`); only modify the configuration file and the environment to allow the service to run.