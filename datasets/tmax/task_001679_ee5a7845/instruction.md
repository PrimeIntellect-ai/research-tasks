You are an IT support technician acting on a critical incident ticket. The `state-sync` daemon, a custom Rust application used to synchronize distributed file states, is currently stuck in an infinite retry loop (convergence failure).

Your task has three phases:
1. **Log Timeline Reconstruction**: In `/home/user/logs/`, you will find logs from three distinct services: `service_a.log`, `service_b.log`, and `state-sync.log`. Merge and sort these logs chronologically to understand the sequence of events. Save the merged chronological log to `/home/user/timeline.log`.
2. **Root Cause Analysis**: Analyze the timeline to identify the exact file path that breaks the parser and triggers the convergence failure. The system uses space-separated logging, but paths are enclosed in double quotes to allow for spaces. However, a bug in the Rust parser breaks when it encounters a file name with spaces. Write the exact file path (without quotes) that caused the crash to `/home/user/bad_file.txt`.
3. **Code Repair**: Navigate to `/home/user/state-sync/`. Fix the format parsing bug in `src/main.rs`. The function `parse_log_line` currently splits by whitespace naively, ignoring the double quotes around the file path. Rewrite `parse_log_line` so that it correctly extracts four fields: `timestamp`, `service`, `file_path` (without the quotes), and `status`. 
4. **Verification**: Compile the fixed project using `cargo build --release`. Run the binary against the state file: `/home/user/state-sync/target/release/state-sync /home/user/logs/state.txt`. If fixed, it will exit cleanly with status 0 and print "Convergence achieved."

**Output Requirements:**
- `/home/user/timeline.log`: A chronologically sorted file containing all lines from the three `.log` files in `/home/user/logs/`.
- `/home/user/bad_file.txt`: A single line containing the exact problematic file path (e.g., `/var/data/my file.txt`).
- The patched Rust project must compile successfully and process `/home/user/logs/state.txt` without getting stuck in an infinite loop.