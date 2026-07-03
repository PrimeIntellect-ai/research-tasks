You are an SRE tasked with setting up a self-healing monitor for a staged deployment system. The system relies on symlinks to manage the active deployment version, and you need to write a script to monitor its health, automatically roll back if necessary, and rotate error logs.

System Overview:
- Configuration file: `/home/user/monitor.conf`. It defines three variables: `DEPLOY_BASE`, `CURRENT_LINK`, and `ARCHIVE_DIR`.
- Deployment history: `/home/user/deployments/history.txt`. This file contains a chronological list of deployment directory names (one per line, e.g., `v1`, `v2`, `v3`), with the last line being the most recent deployment.
- Current active release: A symlink at the path specified by `CURRENT_LINK` that points to the currently active deployment directory inside `DEPLOY_BASE`.

Your Task:
Create and run a script (in any language you choose, e.g., bash, python, perl) saved at `/home/user/run_monitor.sh` (or `.py`, etc.) that performs the following actions exactly in this order:

1. Read Configuration: Parse `/home/user/monitor.conf` to obtain the paths for `DEPLOY_BASE`, `CURRENT_LINK`, and `ARCHIVE_DIR`.
2. Health Check & Rollback: 
   - Read the contents of `health.txt` inside the directory currently pointed to by `CURRENT_LINK`.
   - If the content is exactly `DEGRADED`, you must perform a rollback.
   - To roll back, find the current version's name (the target directory name of the symlink), look it up in `history.txt`, and find the version immediately preceding it. 
   - Update the `CURRENT_LINK` symlink to point to the preceding version directory. (If it is not `DEGRADED`, do not change the symlink).
3. Log Rotation:
   - After ensuring the symlink points to a healthy release (either because no rollback was needed, or because a rollback was just performed), examine the `app.log` file in the *currently active* deployment directory (via `CURRENT_LINK`).
   - If `app.log` contains the exact substring `ERROR`, you must rotate it.
   - To rotate: Move the log file to the `ARCHIVE_DIR`, renaming it to `<version>_app.log.archive` (where `<version>` is the directory name of the active release, e.g., `v2_app.log.archive`). Then, create a new, empty `app.log` in the active deployment directory.

After writing the script, you must execute it once so that the system state is updated according to the rules above.