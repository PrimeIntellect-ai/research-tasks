You are a backup operator testing the automated restore procedures for an internal application stack. You recently restored the application code and its startup scripts to `/home/user/stack_restore`, but the automated startup sequence is failing due to a race condition (similar to a missing `After=` dependency in systemd).

The stack consists of two components:
1. A simulated backend data service (`/home/user/stack_restore/backend_service.sh`), which takes several seconds to initialize before binding to a port.
2. A Rust application (`/home/user/stack_restore/app`), which performs post-restore validation by connecting to the backend.

Currently, the `start_all.sh` script launches the backend in the background and immediately starts the Rust application. The Rust application crashes because the backend is not yet listening.

Your task is to fix the restore sequence by performing the following:

1. **Fix the Rust Application:**
   Navigate to `/home/user/stack_restore/app`. The application currently tries to connect to a hardcoded port. Modify `src/main.rs` so that it reads the backend port from the `BACKEND_PORT` environment variable. If it successfully connects, it should write the exact string `RESTORE_SUCCESS: Verified data connection` to `/home/user/restore_results.log`. Build the application using `cargo build --release`.

2. **Fix the Startup Script:**
   Modify `/home/user/stack_restore/start_all.sh` to properly manage the lifecycle.
   - It must start `backend_service.sh` in the background and redirect its output to `/home/user/stack_restore/backend.log`.
   - Using text processing pipelines (`grep`, `awk`, or similar) and connectivity diagnostics (like `nc` or `curl`), implement a waiting mechanism in `start_all.sh` that polls either the log file or the port. It must wait until the log clearly indicates "Listening for connections" OR the port is actively accepting TCP connections before proceeding.
   - Once the backend is verified as ready, the script should export the `BACKEND_PORT` environment variable (the backend dynamically selects port 8085 for this restore test) and execute the compiled Rust binary (`./app/target/release/restore_verifier`).

3. **Execution:**
   Run `./start_all.sh` to perform the full startup sequence.

Verify your success by ensuring the Rust application completes without panic and `/home/user/restore_results.log` is created with the required success message.