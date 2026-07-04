I need you to help me automate the provisioning and initial backup of a local development service. As an infrastructure engineer, I want to encapsulate this process in a single Python script so we can reuse it. 

Please write a Python script at `/home/user/provision.py` and then run it. The script must perform the following tasks:

1. **Directory & Permission Management**: 
   Ensure the directory `/home/user/backups` exists. If it needs to be created, it must have exactly `0700` permissions.

2. **Process Monitoring and Control**:
   Check if a process running exactly `python3 -m http.server 9999` is active. If it is not running, start it in the background so it continues running after your script exits. Retrieve the Process ID (PID) of this server.

3. **Timezone & Backup Strategy**:
   Determine the current time in the `Asia/Tokyo` timezone, formatted exactly as `YYYY-MM-DD_HH-MM-SS`. 
   Create a compressed tarball (`.tar.gz`) of the existing directory `/home/user/app_data` and save it to `/home/user/backups/app_backup_<tokyo_time>.tar.gz`.

4. **Backup Security**:
   The newly created backup tarball must have its permissions explicitly set to `0600`.

5. **Logging**:
   To allow our automated systems to verify the provisioning, your script must output a strictly valid JSON file at `/home/user/provision.log`. The JSON object must contain exactly these keys:
   - `"pid"`: The integer PID of the `http.server` process.
   - `"backup_file"`: The absolute path string of the generated backup tarball.
   - `"tz"`: The exact string `"Asia/Tokyo"`.

You may use standard library modules or shell commands executed via Python. Ensure you run the script so the final state is achieved.