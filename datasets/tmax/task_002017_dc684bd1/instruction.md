You are an IT support technician responding to an escalated ticket (Ticket #4092). The data science team uses a custom Rust application called `sensor_stats` to process incoming telemetry. Yesterday, the application started crashing with a panic when processing a specific batch of data.

You have been provided with the environment at `/home/user/ticket_4092/`.
Inside this directory, you will find:
1. `sensor_stats/`: The Rust project containing the application source code.
2. `sensor_data.csv`: A large dataset (10,000 lines) that consistently causes the application to crash.

Your tasks are to:
1. **Create a Minimal Reproducible Example (MRE):** The provided `sensor_data.csv` is too large for the developers to step through. Use delta debugging / bisection techniques to find the absolutely minimal subset of lines from `sensor_data.csv` (preserving their original relative order) that triggers the *exact same panic*. Save this minimal dataset to `/home/user/ticket_4092/mre.csv`. It should contain the absolute minimum number of rows required to reproduce the crash.
2. **Diagnose and Fix:** Identify the root cause of the crash in `sensor_stats`. The issue is suspected to be a numerical instability bug leading to a panic. Fix the bug in the Rust code so that it can successfully process the entire `sensor_data.csv` without panicking, while correctly calculating the intended statistics (do not just remove the panic; fix the underlying mathematical instability using a numerically stable algorithm, like Welford's algorithm or a robust two-pass approach).
3. **Verify:** Build the project using `cargo build --release` inside the `sensor_stats` directory. Ensure `cargo run --release -- ../sensor_data.csv` succeeds.
4. **Log Resolution:** Create a log file at `/home/user/ticket_4092/resolution.txt` containing exactly two lines:
   - Line 1: The exact name of the Rust function where the numerical instability originated.
   - Line 2: The number of data lines in your `mre.csv` (excluding headers if your script removed them, or including them if kept; just the `wc -l` count of your MRE file).

Constraints:
- Do not change the command-line interface of the Rust application.
- The fixed application must output standard floating point numbers, not `NaN`.