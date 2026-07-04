You are tasked with fixing and completing a simulated Kubernetes operator that runs on a schedule. The operator is supposed to compile Kubernetes manifests and apply them, but it is currently failing when run via its scheduler wrapper due to missing environment variables and incorrect directory structures. 

The system currently has the following setup:
- A scheduler simulation script at `/home/user/mock-cron.sh`. This script runs the operator script in a completely sanitized environment (simulating a strict cron job).
- The operator script at `/home/user/operator-sync.sh`. It expects certain environment variables to be set, specifically `MANIFEST_DIR`, and requires `kubectl` to be in the system's `PATH`.
- A dummy `kubectl` binary located in `/home/user/dummy-bin/`.
- A directory of existing YAML configurations at `/home/user/legacy-manifests/`.
- A local metrics service running on port `8080`.

Your objectives are:

1. **Environment & Profile Setup:**
   Create a shell profile file at `/home/user/.operator_profile`. This file must export the `MANIFEST_DIR` variable set to `/home/user/operator-data`, and prepend `/home/user/dummy-bin` to the system `PATH`.
   Modify `/home/user/operator-sync.sh` so that the very first thing it does is source `/home/user/.operator_profile`. Do not change the rest of the script's logic.

2. **Directory Structure & Linking:**
   The operator script reads inputs from `$MANIFEST_DIR/inputs/legacy`. Create the necessary directory structure for `MANIFEST_DIR`. Instead of copying the legacy manifests, create a symbolic link from `/home/user/legacy-manifests` to `/home/user/operator-data/inputs/legacy`.

3. **Connectivity Diagnostics Script:**
   Create a new bash script at `/home/user/check_metrics.sh`. This script must test connectivity to the local metrics service on `127.0.0.1:8080` (you can use `curl` or `nc`). 
   - If the service is reachable, the script should output exactly `METRICS_UP=1` and append this line to `/home/user/operator-data/outputs/status.log`.
   - Ensure the script is executable.

4. **Execution & Verification:**
   - Run `/home/user/mock-cron.sh`. If you configured the environment and links correctly, it will successfully create `/home/user/operator-data/outputs/compiled.yaml` containing the concatenated legacy manifests, and write a log to `$MANIFEST_DIR/operator.log`.
   - Run your `/home/user/check_metrics.sh` script to verify connectivity and generate the `status.log`.

Final expected state to be verified:
- `/home/user/operator-data/inputs/legacy` is a valid symlink to `/home/user/legacy-manifests`.
- `/home/user/operator-data/outputs/compiled.yaml` exists and contains the concatenated configuration.
- `/home/user/operator-data/operator.log` exists.
- `/home/user/operator-data/outputs/status.log` exists and contains `METRICS_UP=1`.