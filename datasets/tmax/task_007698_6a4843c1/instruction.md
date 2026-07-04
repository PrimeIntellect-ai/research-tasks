You are a developer tasked with debugging a failing build system in a forensics scenario. 

You have been given access to a build workspace at `/home/user/workspace`. The automated build script, `./build.sh`, is failing and producing incorrect artifacts. 

Upon initial investigation, the previous developer left behind a `build_error.log` which contains a Bash stack trace showing a crash, alongside some corrupted output files.

Your objectives are:
1. **Analyze and Fix Recursion:** The script `process_assets.sh` (called by `build.sh`) crashes due to an infinite recursion issue. Analyze the script and the directory structure to find the root cause (hint: look out for filesystem loops). Fix `process_assets.sh` so it terminates correctly without throwing errors, while still processing all regular files.
2. **Analyze and Fix Race Condition:** The build spawns multiple background jobs (`compile.sh` and `process_assets.sh`) that concurrently read and update a shared file `/home/user/workspace/manifest.txt` to register processed files. Due to a race condition, entries are being lost. Modify the relevant scripts to ensure atomic updates to `manifest.txt` (e.g., using `flock`).
3. **Create a Minimal Reproducible Example:** Create a new standalone script at `/home/user/workspace/mre_race.sh` that isolates and minimally reproduces the file-update race condition *as it originally existed* (before your fix). This script should spawn 10 background bash functions that simultaneously read, append, and overwrite a file named `mre_test.txt` without locking, demonstrating data loss.
4. **Final Build:** Once fixed, clean the workspace of old artifacts (remove `manifest.txt`) and run `./build.sh`. If successful, the script will naturally terminate and `manifest.txt` will contain exactly 200 registered lines.

**Deliverables:**
- The patched `process_assets.sh` and `compile.sh`.
- The isolated bug reproduction script `/home/user/workspace/mre_race.sh`.
- The successfully generated `/home/user/workspace/manifest.txt` (created by running `./build.sh` after applying your fixes).