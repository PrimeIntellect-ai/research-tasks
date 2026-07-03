You are an infrastructure engineer automating the provisioning pipeline for user-level services. We need to set up a directory-watcher daemon using a bash script and systemd user services, along with a health check script.

Please complete the following tasks exclusively in `/home/user`:

1. **Directories**: Create two directories: `/home/user/provision_inbox` and `/home/user/provision_archive`.
2. **Watcher Script**: Create an executable bash script at `/home/user/watcher.sh`. When run, it should:
   - Find all files ending in `.txt` in `/home/user/provision_inbox`.
   - Move each found file to `/home/user/provision_archive`.
   - For every moved file, append the exact line `PROVISIONED: <filename>` (e.g., `PROVISIONED: app1.txt`) to `/home/user/provision.log`.
3. **Systemd User Service**: Create a systemd user service file at `/home/user/.config/systemd/user/provision-watcher.service` that executes `/home/user/watcher.sh`. Set the description to "Provision Watcher".
4. **Systemd Timer**: Create a systemd timer file at `/home/user/.config/systemd/user/provision-watcher.timer` that triggers the `provision-watcher.service` every 2 minutes (`OnCalendar=*:0/2`).
5. **Health Check Script**: Create an executable bash script at `/home/user/health.sh`. It should check if `/home/user/provision.log` exists.
   - If it exists, print `STATUS: OK` to standard output.
   - If it does not exist, print `STATUS: PENDING` to standard output.

Ensure all scripts have the correct execution permissions. Do not attempt to start or enable the systemd services, just create the valid unit files.