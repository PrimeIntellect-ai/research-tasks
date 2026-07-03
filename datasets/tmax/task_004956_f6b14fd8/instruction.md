You are a Cloud Architect migrating storage services to a new platform. You need to build a continuous deployment pipeline for a custom Rust-based data migration daemon. Since you do not have root access on this staging environment, you will use standard Linux user-space tools to simulate service management and filesystem mounting.

Your task is to implement this system completely within `/home/user`.

Follow these requirements precisely:

1. **Directory Structure & Setup:**
   - Create the following directories: `/home/user/logs`, `/home/user/config`, `/home/user/bin`, `/home/user/run`, `/home/user/old_data`, and `/home/user/deploy_worktree`.
   - Create a file `/home/user/old_data/hello.txt` with the exact content: `MIGRATION_READY`.
   - Create a configuration file at `/home/user/config/virtual_fstab` containing exactly one line of text:
     `/home/user/old_data /home/user/new_data/mnt`
     (This simulates an fstab entry mapping a source to a destination).

2. **Git Repository & Hook:**
   - Initialize a bare Git repository at `/home/user/migration_repo.git`.
   - Configure a `post-receive` hook in this bare repository.
   - The hook must:
     a) Checkout the pushed code into `/home/user/deploy_worktree`.
     b) Navigate to `/home/user/deploy_worktree/migrator`.
     c) Compile the Rust project using `cargo build --release`.
     d) Execute the service restart script at `/home/user/bin/restart_service.sh`.
   - Ensure the hook is executable.

3. **Service Management Script:**
   - Create a bash script at `/home/user/bin/restart_service.sh` and make it executable.
   - This script must:
     a) Read the PID from `/home/user/run/migrator.pid`.
     b) If the PID exists and the process is running, kill it gracefully.
     c) Start the newly compiled Rust binary (`/home/user/deploy_worktree/migrator/target/release/migrator`) in the background.
     d) Write the background process's new PID to `/home/user/run/migrator.pid`.

4. **The Rust Migrator Daemon:**
   - Clone the bare repository to a workspace at `/home/user/workspace`.
   - Inside the workspace, initialize a Rust binary project named `migrator`.
   - Write the Rust code in `main.rs` so that upon starting, it:
     a) Reads `/home/user/config/virtual_fstab`.
     b) Parses the source and destination paths.
     c) Ensures the parent directory for the destination exists (e.g., creates `/home/user/new_data`).
     d) Creates a Unix symlink at the destination path pointing to the source path (simulating a bind mount).
     e) Appends the exact line `MOUNTED <source> TO <destination>` (e.g., `MOUNTED /home/user/old_data TO /home/user/new_data/mnt`) to `/home/user/logs/migration.log`.
     f) Enters an infinite loop, sleeping for 10 seconds per iteration (to act as a long-running daemon).

5. **Execution:**
   - Commit the Rust project in your `/home/user/workspace` repository.
   - Push the `master` branch to the bare repository at `/home/user/migration_repo.git`.
   - The push should successfully trigger the hook, build the project, restart the daemon, create the symlink, and write the log.

Verify that the end-to-end pipeline works: pushing code should result in the daemon running, the log file being populated, and `/home/user/new_data/mnt/hello.txt` successfully exposing the contents of the old data directory.