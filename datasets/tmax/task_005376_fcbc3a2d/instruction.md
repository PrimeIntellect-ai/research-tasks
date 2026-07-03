You are managing a mock Kubernetes operator environment that processes Ingress manifests. Part of the operator's job is to perform a pre-flight connectivity diagnostic on the domains specified in the manifests, quarantine invalid ones, and update the mailing list server configuration to notify administrators.

Your task is to write and execute a Bash script at `/home/user/check_ingress.sh` that automates this process. 

The environment has the following structure:
- `/home/user/k8s-operator/manifests/` : Contains `.yaml` Ingress manifests.
- `/home/user/k8s-operator/quarantine/` : An initially empty directory for bad manifests.
- `/home/user/k8s-operator/alerts/` : An initially empty directory for alert logs.
- `/home/user/k8s-operator/mail_config.rc` : The system configuration file for the mailer daemon.

Your script `/home/user/check_ingress.sh` must do the following:
1. Iterate over every `.yaml` file in `/home/user/k8s-operator/manifests/`.
2. Extract the domain name from the file. You can assume the domain is defined on a line exactly matching the pattern: `  host: <domain>` (two spaces, "host:", one space, and the domain name).
3. Perform a connectivity diagnostic on the extracted domain using the `ping` command (send exactly 1 packet with a 1-second timeout).
4. If the `ping` command fails (exit code non-zero):
   - Move that `.yaml` file into `/home/user/k8s-operator/quarantine/`.
   - Append the failing domain name (just the domain, nothing else) on a new line to `/home/user/k8s-operator/alerts/dns_failures.log`.
   - Ensure a line exactly reading `ALERT_TRIGGERED=1` is appended to `/home/user/k8s-operator/mail_config.rc` (do this only once, or once per failure, either is fine as long as it's present if a failure occurred).

Constraints:
- Use only standard bash built-ins and coreutils (e.g., `grep`, `awk`, `ping`, `mv`, `echo`). 
- After creating the script, you must execute it so the final state of the filesystem is updated.