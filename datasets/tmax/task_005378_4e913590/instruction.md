You are an infrastructure engineer automating a local provisioning pipeline. We do not have root access, so we are simulating some system-level configurations.

Your task is to create and execute a Python script at `/home/user/bin/deploy_pipeline.py` that acts as a local CI/CD deployment runner. The script must perform the following actions automatically when run:

1. Read a deployment payload from a JSON file located at `/home/user/ci_webhook.json`. The JSON file has the following structure:
   ```json
   {
       "artifact": "/home/user/build/app.zip",
       "target_dir": "/home/user/app_root",
       "disk_image": "/home/user/storage.img",
       "mount_point": "/home/user/app_root/storage"
   }
   ```

2. Extract the zip file specified in the `artifact` field into the directory specified in `target_dir`. (Create `target_dir` if it does not exist).

3. Simulate a mount configuration by appending exactly the following line to `/home/user/mock_fstab`:
   `[disk_image] [mount_point] ext4 defaults 0 2`
   (Replace `[disk_image]` and `[mount_point]` with the exact values from the JSON file).

4. Configure a scheduled task to monitor the application. Write a crontab entry for the current user that runs the extracted script `healthcheck.py` every 5 minutes. The exact crontab line must be:
   `*/5 * * * * /usr/bin/python3 /home/user/app_root/healthcheck.py >> /home/user/health.log 2>&1`
   Ensure you don't overwrite existing cron jobs if there are any (though you can assume the crontab might be empty initially). 

5. Start the application process. Run `/home/user/app_root/server.py` using `python3` in the background. Capture its Process ID (PID) and write it to `/home/user/app_root/server.pid`.

After writing `/home/user/bin/deploy_pipeline.py`, you must execute it so that the deployment actually occurs based on the existing `/home/user/ci_webhook.json`.