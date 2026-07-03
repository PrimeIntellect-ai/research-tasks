You are acting as a capacity planner analyzing network resource usage. We have a C program that logs simulated network statistics, but it currently writes its output to whatever the current working directory is, which causes logs to get lost when triggered by automated background tasks (like Git hooks). 

Your objective is to fix the C program, set up a local bare Git repository to act as a trigger, configure a Git hook to run the program, write an Expect script to automate triggering it, and set up log rotation for the output.

Here are your specific instructions:

1. **Fix the C Program**:
   There is a C program located at `/home/user/src/net_monitor.c`. Currently, it uses `fopen("net_stats.log", "a")`. Modify this program so that it reads an environment variable named `LOG_DIR`. If `LOG_DIR` is set, it should write to `$LOG_DIR/net_stats.log`. If `LOG_DIR` is not set, it should default to `/tmp/net_stats.log`. Recompile is not needed immediately as the hook will do it.

2. **Directory Structure**:
   Create the directories `/home/user/logs` and `/home/user/bin` if they do not exist.

3. **Git Server Setup**:
   Initialize a bare Git repository at `/home/user/git/capacity.git`.

4. **Git Hook Configuration**:
   Create a `post-receive` hook in the bare repository (`/home/user/git/capacity.git/hooks/post-receive`). The hook must do the following when a push is received:
   - Compile `/home/user/src/net_monitor.c` into an executable at `/home/user/bin/net_monitor`.
   - Export the environment variable `LOG_DIR=/home/user/logs`.
   - Execute `/home/user/bin/net_monitor`.
   Make sure the hook is executable.

5. **Expect Scripting for Automation**:
   Write an Expect script at `/home/user/simulate_push.exp`. When executed, this script must:
   - Clone the bare repository `/home/user/git/capacity.git` into `/home/user/capacity_clone`.
   - Change directory into `/home/user/capacity_clone`.
   - Create an empty file named `trigger.txt`.
   - Git add, commit (with message "Trigger network monitor"), and push the changes back to the origin.
   Ensure the Expect script handles the necessary prompts or standard output seamlessly and is marked as executable.

6. **Log Configuration**:
   Create a logrotate configuration file at `/home/user/logrotate.conf` specifically to manage `/home/user/logs/net_stats.log`. The configuration should specify:
   - Daily rotation.
   - Keep 5 days of backlogs (rotate 5).
   - Compress the old log files.
   - Ignore errors if the log file is missing (`missingok`).

Run your Expect script once to ensure everything works and `/home/user/logs/net_stats.log` is generated successfully.