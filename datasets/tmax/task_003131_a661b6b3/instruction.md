You are tasked with writing a Bash-based mock "Kubernetes Operator" script that manages manifest files through symbolic links and directory structures, while providing a continuous health check.

Write a bash script at `/home/user/operator.sh` that does the following:

1. **Idempotent Setup**: When started, the script must ensure the following directories exist:
   - `/home/user/k8s/src`
   - `/home/user/k8s/live`
   - `/home/user/k8s/archive`

2. **Continuous Reconciliation Loop**: The script must run an infinite loop that iterates every 2 seconds (`sleep 2`).

3. **Manifest Management**: Inside the loop, the script must process all `.yaml` files in `/home/user/k8s/src`.
   - It should read the first line of each file.
   - If the first line is exactly `# DEPLOY_STATE: active`, the script must ensure a symbolic link to this file exists in `/home/user/k8s/live/` with the same filename.
   - If the first line is exactly `# DEPLOY_STATE: archived`, the script must:
     a) Remove the symbolic link from `/home/user/k8s/live/` (if it exists).
     b) Move the `.yaml` file from `/home/user/k8s/src/` to `/home/user/k8s/archive/`.
   - Any other first line (or missing line) should be ignored.

4. **Health Check Monitoring**: At the end of every loop iteration (before sleeping), the script must overwrite the file `/home/user/operator.status` with exactly two lines:
   - The first line must contain the PID of the running script.
   - The second line must contain the current Unix epoch timestamp (using `date +%s`).

After writing the script, make it executable and start it in the background. Ensure it keeps running so that the system state can be verified by automated tests adding and modifying files in `/home/user/k8s/src`.