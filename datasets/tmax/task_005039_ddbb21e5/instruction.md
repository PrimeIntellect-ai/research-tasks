You are an infrastructure specialist managing a set of microservices running in a containerized environment. Since you do not have root privileges to create real bind mounts, you need to simulate them using symbolic links based on a custom `fstab`-like configuration file.

Your task is to write and execute an automation script (in any language you prefer) that parses a configuration file, checks which microservices are currently running, and sets up simulated "mounts" (symlinks) for the active ones.

**Configuration File:**
There is a file at `/home/user/micro_fstab` with space-separated columns, mimicking an fstab file:
`<source_directory> <mount_point_symlink> <service_process_name>`

**Requirements for your script:**
1. **Parse `/home/user/micro_fstab`**: Read all entries.
2. **Process Monitoring**: For each entry, check if a process with the exact `<service_process_name>` is currently running.
3. **Directory and Link Management**: 
   - If the service process **is running**: Ensure the `<source_directory>` exists (create it if it doesn't). Then, create a symbolic link at `<mount_point_symlink>` pointing to the `<source_directory>`. 
   - If the service process **is not running**: Ensure that NO file or symlink exists at `<mount_point_symlink>` (remove it if it does).
4. **Automation & Reporting**: Write your script to `/home/user/sync_mounts` (e.g., `sync_mounts.py` or `sync_mounts.sh`) and execute it. 
5. **Output Log**: Your script must generate a JSON file at `/home/user/service_report.json` summarizing the final state. The keys should be the service process names, and the values should be a boolean (`true` if running and symlinked, `false` if not running).

**JSON Output Format Example:**
```json
{
  "auth_service": true,
  "cache_service": false
}
```

Write and run the script to bring the system state into alignment with the `micro_fstab` definitions.