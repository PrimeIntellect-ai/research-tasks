You are a monitoring specialist tasked with setting up an automated network and storage alert system. Due to permissions, we are using user-level configurations and simulating a few root-level components. 

You need to integrate an interactive network diagnostic tool, a simulated `fstab` configuration, and a Git repository that acts as an alert trigger.

Follow these steps exactly:

1. **Storage Configuration (fstab simulation):**
   Create a file at `/home/user/my_fstab`. Add a single line representing a mount configuration that maps the remote share `/home/user/remote_share` to the local mount point `/home/user/mnt/backup`. Set the filesystem type to `nfs` and the options to `defaults,ro`. Ensure the directories `/home/user/remote_share` and `/home/user/mnt/backup` exist.

2. **Alert Repository (Git Server & Hook):**
   Create a bare Git repository at `/home/user/monitor.git`. 
   Configure a `post-receive` hook in this bare repository. The hook must be an executable shell script that, whenever a push is received, appends the exact string `ALERT: Network configuration changed` to `/home/user/alerts.log`.

3. **Interactive Script Automation (Expect):**
   There is an interactive diagnostic script located at `/home/user/tools/check_net.sh`. When run, it prompts for credentials and a target configuration file.
   Write an automation script (using Expect, Python pexpect, or a similar tool) at `/home/user/run_check.exp`. Your automation script must:
   - Run `/home/user/tools/check_net.sh`.
   - Wait for the prompt `Enter username:` and send `admin`.
   - Wait for the prompt `Enter pin:` and send `8492`.
   - Wait for the prompt `Enter target file:` and send `/home/user/my_fstab`.
   - Capture the final successful output string printed by the tool.

4. **Integration and Execution:**
   - Clone the bare repository `/home/user/monitor.git` to a local working directory at `/home/user/monitor_local`.
   - Extend your automation script (or write a wrapper) so that after running the interactive tool, it takes the final successful output string, writes it to a file named `status.txt` inside `/home/user/monitor_local`, commits the file with the message "Update status", and pushes it to `origin master`.
   - Run your automation script so that the push occurs, triggering the `post-receive` hook and generating the `/home/user/alerts.log` file.