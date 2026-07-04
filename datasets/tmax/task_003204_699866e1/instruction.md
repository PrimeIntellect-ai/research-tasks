You are an observability engineer tuning dashboards for network storage health. You need to implement a staged rollout of a custom Bash-based monitoring daemon that checks network file system mounts. Since you don't have access to systemd on this container, you will build a custom process supervisor in Bash.

Write a master deployment script at `/home/user/rollout_monitors.sh` that performs the following tasks:

1. **Fstab Parsing:**
   Read the mock fstab file located at `/home/user/mock_fstab`. Extract the exact mount point (the second column) for the entry that has the filesystem type `nfs4`.

2. **Daemon Creation:**
   Create a script at `/home/user/daemon.sh` that takes a mount point as its first argument. It should loop infinitely, echoing `HEARTBEAT <mount_point>` to `STDOUT`, sleeping for 0.1 seconds between each echo. 

3. **Supervisor Creation:**
   Create a script at `/home/user/supervisor.sh` that takes two arguments: `<stage>` and `<mount_point>`. 
   - It should continuously run `/home/user/daemon.sh <mount_point>` in the foreground.
   - It should redirect the daemon's output to `/home/user/logs/<stage>.log`.
   - If the daemon crashes or exits, the supervisor must immediately restart it (an infinite restart loop).

4. **Staged Deployment:**
   The master script (`rollout_monitors.sh`) must execute a staged deployment:
   - Make sure `/home/user/logs/` directory exists.
   - Stage 1 (Canary): Start `/home/user/supervisor.sh canary <mount_point>` as a background process.
   - Monitor `/home/user/logs/canary.log`. Wait until there are at least 10 lines in the log.
   - Stage 2 (Prod): Once Canary is validated (10 lines generated), start `/home/user/supervisor.sh prod <mount_point>` as a background process.
   - Monitor `/home/user/logs/prod.log`. Wait until there are at least 10 lines in the log.
   - Finalization: Once both stages are running and have generated 10+ log lines, write the extracted mount point to `/home/user/success.txt`.

Ensure all scripts you create are made executable. You must write and execute `/home/user/rollout_monitors.sh` to complete the task. Leave the background processes running when your script exits.