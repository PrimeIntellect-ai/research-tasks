You are a deployment engineer rolling out a new update for an internal backend service. The target environment doesn't use standard init systems (like systemd) due to legacy container constraints, and you do not have root privileges. You need to handle process monitoring, simulate an email alert for the mailing list, and prepare a mount configuration for the deployment package.

Perform the following tasks:

1. **Mount Configuration Preparation**: 
   The worker process will eventually need access to a read-only NFS share. Create a file named `/home/user/deploy_fstab`. It must contain exactly one line with the following standard fstab format to mount `nfs.internal.net:/vol/data` to `/home/user/worker_data` using the `nfs` filesystem type, with options `defaults,ro`, and dump/pass values of `0 0`.

2. **Alert Mail Spool Setup**:
   Ensure the directory `/home/user/mail_spool` exists. This will be used to spool simulated email alerts for the on-call mailing list.

3. **Process Monitor & Health Check Script**:
   There is a flaky script located at `/home/user/worker.sh` that crashes periodically. You must write a Bash script named `/home/user/manager.sh` that acts as a deployment health monitor. 
   
   The `/home/user/manager.sh` script must:
   - Execute `/home/user/worker.sh`.
   - Wait for it to finish and capture its exit code.
   - If the exit code is non-zero, append exactly this line to `/home/user/mail_spool/alerts.txt`:
     `ALERT: Worker crashed with code X` (where X is the actual exit code).
   - The manager should restart the worker process if it fails.
   - To prevent an infinite restart loop during this rollout test, the manager must attempt to run the worker **exactly 3 times**. After the worker completes (or crashes) for the 3rd time, the `manager.sh` script must exit with a status code of `0`.

4. **Execution**:
   Make `/home/user/manager.sh` executable and run it once so that it populates the `alerts.txt` file based on the behavior of `/home/user/worker.sh`.