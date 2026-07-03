You are tasked with fixing and configuring a local mock Kubernetes operator deployment that manages manifests via Git. The system consists of user-level `systemd` services, a local Git server, and interactive deployment scripts.

Your goals are to resolve a service dependency issue, configure a Git hook, automate an interactive push using `expect`, and configure log rotation.

Perform the following tasks:

1. **Fix the Operator Service Dependency:**
   There are two user-level systemd services: `k8s-mock-api.service` and `manifest-operator.service` located in `/home/user/.config/systemd/user/`.
   The `manifest-operator.service` currently fails to start reliably because it attempts to connect to the mock API before it is ready. Modify `/home/user/.config/systemd/user/manifest-operator.service` so that it starts *after* `k8s-mock-api.service` and requires it. Reload the systemd user daemon and enable/start both services.

2. **Configure the Git Hook:**
   There is a bare Git repository at `/home/user/k8s-manifests.git` representing the cluster state.
   Create a `post-receive` hook in `/home/user/k8s-manifests.git/hooks/post-receive`. Ensure it is executable.
   When a push is received, the hook must read from standard input (which Git provides as `<oldrev> <newrev> <refname>`) and append the following exact line to `/home/user/operator-logs/hook.log`:
   `HOOK_TRIGGERED: <newrev>` (replace `<newrev>` with the actual new commit hash).

3. **Automate the Deployment Script:**
   There is a local workspace clone at `/home/user/workspace/k8s-manifests`. To push changes, developers use a wrapper script located at `/home/user/push-manifests.sh`. This script interactively prompts for a passphrase.
   Write an `expect` script at `/home/user/auto-push.exp` that:
   - Spawns the `/home/user/push-manifests.sh` script.
   - Waits for the exact prompt: `Deploy Passphrase: `
   - Sends the passphrase `k8s-oper-2024\r`
   - Waits for the process to complete successfully.
   Ensure the expect script is executable.

4. **Configure Log Rotation:**
   The operator and hooks write logs to `/home/user/operator-logs/`. Create a logrotate configuration file at `/home/user/logrotate.conf` that targets `/home/user/operator-logs/*.log` with the following rules:
   - Rotate daily
   - Keep exactly 3 rotated copies
   - Compress the rotated logs

Ensure all files are owned by `user` and placed in the exact paths specified.