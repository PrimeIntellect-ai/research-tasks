You are acting as a backup operator testing an automated restore pipeline. During a recent test, a restored systemd service failed to start properly because it was missing its dependency definitions. 

You need to write an idempotent Python configuration script that fixes this issue automatically. This script will be integrated into our CI/CD pipeline.

Here are your requirements:

1. Look in the directory `/home/user/workspace/`. You will find two files:
   - `backup_manifest.log`: A text log from the backup system.
   - `app.service`: The restored systemd service configuration file.

2. Create a Python script at `/home/user/fix_service.py` that does the following:
   - Parses `/home/user/workspace/backup_manifest.log` to extract the required service dependency. Look for the line starting with "Requires System Service: " and extract the service name that follows it.
   - Modifies `/home/user/workspace/app.service` by adding two lines under the `[Unit]` section:
     `After=<extracted_service_name>`
     `Wants=<extracted_service_name>`
   - The script **must be idempotent**. If the `After=` and `Wants=` lines for that specific service already exist in the `[Unit]` section, the file should not be changed. Do not add duplicate entries.
   - Once complete, the script must write a single line to `/home/user/workspace/restore_status.txt`.
     - If changes were made to the service file, write exactly: `SUCCESS: Added <extracted_service_name>`
     - If the file already contained the correct entries and no changes were made, write exactly: `SUCCESS: Already configured`

3. After writing the script, execute it once so that `app.service` is fixed and the `restore_status.txt` file is generated. 

Ensure your Python script strictly follows the requirements and handles the standard INI-like format of a systemd service file without removing existing settings.