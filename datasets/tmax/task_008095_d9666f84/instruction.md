You are tasked with setting up a custom process health-monitoring daemon written in Rust. As a system administrator managing restricted environments, you often need custom user-space tools to monitor background processes. 

A setup script has already created a file at `/home/user/monitored_pids.txt` containing a list of Process IDs (PIDs), one per line. Some of these processes are currently running, and some are not.

Your objective is to:
1. Initialize a new Rust binary project in the directory `/home/user/health_monitor`.
2. Write a Rust application that reads `/home/user/monitored_pids.txt`.
3. The program must check the status of each PID listed in the file. A process is considered "active" if it is currently running (e.g., its directory exists in `/proc`), and "inactive" otherwise.
4. The program must write the results to a JSON file at `/home/user/status.json`. The JSON format must be a single flat object mapping the PID string to its status string ("active" or "inactive"). For example:
   ```json
   {
     "1024": "active",
     "999999": "inactive",
     "1025": "active"
   }
   ```
5. The Rust program must run continuously as a daemon-like background process, performing this check and overwriting the `/home/user/status.json` file every 1 second.
6. Compile the Rust project in release mode.
7. Execute the compiled binary so it runs in the background. You must leave the program running when you complete your task.

Do not use any external Rust crates (like `sysinfo` or `serde_json`) to keep the build fast and offline-compatible; rely entirely on the Rust standard library (e.g., `std::fs`, `std::thread`, `std::time`, and manual string formatting for the simple JSON).

Ensure the background process is actively running and `/home/user/status.json` exists and is correctly populated before you finish.