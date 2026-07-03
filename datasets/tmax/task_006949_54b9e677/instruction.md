You are an observability engineer tasked with exposing metrics from a legacy application so our dashboarding tools can scrape them. The legacy application writes logs to `/home/user/legacy_app.log`. We need a custom Prometheus metrics exporter written in Rust and a small automation script to serve it.

Please complete the following steps:

1. **Backup**: First, create a backup of the log file at `/home/user/backup/legacy_app.log.bak`.
2. **Rust Exporter**: Write a standalone Rust program at `/home/user/exporter.rs` (do not use Cargo, just a single file). The program must read `/home/user/legacy_app.log` and count the total number of lines containing the exact substring `[ERROR]` and the exact substring `[WARN]`.
3. **Metrics Format**: The Rust program must write the results to `/home/user/metrics/metrics.txt` in the following exact Prometheus-compatible format:
   ```
   # HELP legacy_app_errors Total errors
   # TYPE legacy_app_errors counter
   legacy_app_errors <error_count>
   # HELP legacy_app_warnings Total warnings
   # TYPE legacy_app_warnings counter
   legacy_app_warnings <warn_count>
   ```
   *(Replace `<error_count>` and `<warn_count>` with the actual integer counts).*
4. **Compile**: Compile your Rust program to the binary `/home/user/exporter`. 
5. **Automation Script**: Create a bash script at `/home/user/run_exporter.sh`. When executed, this script should:
   - Run the `/home/user/exporter` binary to generate the `metrics.txt` file.
   - Start a simple HTTP server on port `9090` that serves the contents of the `/home/user/metrics` directory. (Using `python3 -m http.server 9090` is perfectly acceptable). 
   - Ensure the script is executable.
   - Ensure the server runs in the background (using `&`) so the script returns successfully without blocking.
6. **Execution**: Run your `/home/user/run_exporter.sh` script so the server is actively listening on port 9090.

Ensure all paths match exactly and the web server is running when you finish the task.