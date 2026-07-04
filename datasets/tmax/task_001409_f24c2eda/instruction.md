You are an observability engineer tasked with tuning a local metrics ingestion pipeline. The current pipeline uses a lightweight C-based log aggregator that processes incoming metric streams, but we are experiencing two major issues: "ERROR" metrics are being silently dropped (similar to an SSH config silently rejecting key-based logins), and the timestamps on our dashboards are out of sync because the aggregator is not explicitly using the required timezone.

Your objective is to fix the aggregator, configure the system parameters for the deployment, and create a deployment script.

Here are your specific tasks:

1. **Fix the Aggregator (`/home/user/proxy.c`)**
   There is a C program located at `/home/user/proxy.c`. It reads lines from standard input and logs them to `/home/user/metrics_data/metrics.log` with a timestamp. 
   - Find and fix the bug in the C code that causes it to silently drop any line containing the word "ERROR".
   - Ensure the program logs using the `Europe/Zurich` timezone. You can achieve this by modifying the C code or explicitly setting the environment in your deployment script.

2. **Storage Configuration (`/home/user/fstab_entry.txt`)**
   We are preparing to mount a dedicated XFS volume for the metrics directory, but since you lack root access to run `mount` right now, you must draft the exact `fstab` configuration.
   - Create a file at `/home/user/fstab_entry.txt`.
   - Write a single valid `fstab` line that mounts a volume with `UUID=1234-5678` to `/home/user/metrics_data` using the `xfs` filesystem. Use the mount options `defaults,noatime` and set dump/pass to `0 0`.

3. **CI/CD Deployment & Notification Script (`/home/user/deploy.sh`)**
   Write a bash script at `/home/user/deploy.sh` that automates the deployment and testing of the aggregator.
   The script must:
   - Be executable.
   - Create the directory `/home/user/metrics_data` if it doesn't exist.
   - Compile `/home/user/proxy.c` into an executable at `/home/user/proxy_bin`.
   - Test the binary by piping the contents of `/home/user/test_metrics.txt` (which already exists) into `/home/user/proxy_bin`.
   - Simulate sending an email to the observability mailing list by appending a properly formatted email message to `/home/user/mail.mbox`. The appended email must have exactly these headers and body format:

     ```
     To: observability-alerts@local.dev
     Subject: Deployment successful
     
     The metrics proxy has been deployed.
     ```

Make sure you complete all steps and leave the `/home/user/deploy.sh` script ready to be executed by our automated test suite. Do not change the logging format string in the C code, only fix the dropping behavior and timezone.