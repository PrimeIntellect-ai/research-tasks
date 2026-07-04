You are acting as a capacity planner and system administrator. We have an old metrics aggregation pipeline that runs via a simulated cron job, but it frequently fails because it writes reports to the wrong hardcoded location due to missing environment variables. Additionally, the metrics source now requires interactive authentication, breaking our old automated scripts.

Your task is to fix the pipeline, introduce an automated interactive login, and perform a staged deployment of the fixed Rust metrics analyzer.

Here are your specific requirements:

1. **Automate Interactive CLI Setup (`/home/user/fetch_metrics.exp`)**
   We have a dummy CLI tool at `/home/user/cap_cli.sh` that provides capacity metrics (CSV format). It now prompts for a password.
   Write an `expect` script at `/home/user/fetch_metrics.exp` that:
   - Spawns `/home/user/cap_cli.sh`.
   - Waits for the password prompt.
   - Sends the password `cap123`.
   - Captures and outputs the resulting CSV data to stdout.

2. **Fix the Rust Analyzer (`/home/user/analyzer/src/main.rs`)**
   There is a Rust project at `/home/user/analyzer`. It is designed to read CSV lines from standard input (format: `hostname,cpu_usage,mem_usage`), sum the `mem_usage` values, and write `Total Mem: <sum>` to a file. 
   - Currently, it has a bug where it hardcodes the output path to `/tmp/wrong_path.txt` (a common issue when running via cron with a stripped PATH/env).
   - Modify `/home/user/analyzer/src/main.rs` so that it reads the environment variable `REPORT_PATH`. If `REPORT_PATH` is set, it must write the output to that path. If it is not set, it should default to `report.txt` in the current working directory.

3. **Create a Staged Deployment Script (`/home/user/deploy.sh`)**
   Write a bash script at `/home/user/deploy.sh` that performs the following:
   - Compiles the Rust project in `/home/user/analyzer` using `cargo build --release`.
   - Simulates a rolling deployment by copying the compiled binary (`target/release/analyzer`) to `/home/user/bin/analyzer_v2`.
   - Atomically updates the symlink at `/home/user/bin/analyzer` to point to `/home/user/bin/analyzer_v2`.
   - Executes your expect script (`/home/user/fetch_metrics.exp`), pipes its output into the newly deployed binary (`/home/user/bin/analyzer`), and ensures the environment variable `REPORT_PATH` is set to `/home/user/final_report.txt` during this execution.

Make sure your `deploy.sh` script works end-to-end. Do not run it automatically; we will run `/home/user/deploy.sh` to verify your solution.