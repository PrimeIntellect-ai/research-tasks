You are acting as a monitoring specialist tasked with setting up a local alert system to detect network misconfigurations in our containerized services. We have several service logs located in `/home/user/logs/`. Some of these services are failing to reach each other due to recent network changes.

Your objective is to parse these logs, organize the failing ones, and stage an email alert.

Please complete the following steps:

1. **Log Parsing & Organization**: 
   Search through all `.log` files in `/home/user/logs/`. You are looking for lines matching the exact pattern: `[ERROR] Connection to <target_service> failed:` (where `<target_service>` is a variable service name).
   Create a directory `/home/user/alerts/active/`. For every log file that contains at least one of these networking errors, create a symbolic link to that log file inside `/home/user/alerts/active/`. The symlink must have the exact same name as the original log file.

2. **Alert Email Generation**:
   Extract the source service (the name of the log file without the `.log` extension) and the target service it is failing to reach.
   Create an email spool file at `/home/user/spool/mail/network_alerts.txt`. (You will need to create the directory structure).
   The file must have the following exact format:
   ```
   To: admin@monitoring.local
   Subject: Network Alerts
   
   ALERT: <source_service> cannot reach <target_service>
   ALERT: <source_service> cannot reach <target_service>
   ```
   *Note: Sort the `ALERT:` lines alphabetically by `<source_service>`.*

3. **Permissions**:
   Because email spool files can contain sensitive internal network topologies, set the permissions of `/home/user/spool/mail/network_alerts.txt` to be strictly read and write for the owner only (`600`).

Do not use root/sudo for any of these operations. Write your commands entirely in Bash.