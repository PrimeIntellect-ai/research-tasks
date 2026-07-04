You are assisting a backup operator in testing a recovery procedure. We recently performed a test restore of an application into `/home/user/app_restore/`. However, the automated restore validation is silently failing because the application's configuration retains the source server's settings, effectively locking out the validation tools. 

Specifically, the configuration file at `/home/user/app_restore/config.ini` has `AllowAutomatedRestore=false` and `Timezone=America/New_York`.

Your task is to create and run a health check script (you may use Bash, Python, or any other language available on standard Linux systems) that prepares the restored data for validation. The script must perform the following actions:

1. Modify the `/home/user/app_restore/config.ini` file in-place to change `AllowAutomatedRestore` to `true` and `Timezone` to `UTC`. Leave any other lines in the file intact.
2. Monitor the simulated storage quota by calculating the total apparent size in bytes of the `/home/user/app_restore/data/` directory. You must use the exact logic of `du -sb /home/user/app_restore/data/ | awk '{print $1}'` to determine this integer value.
3. Generate a health report log at `/home/user/restore_status.json`. The file must contain strictly valid JSON with the following schema:
   ```json
   {
     "status": "ready",
     "data_size_bytes": <integer_size_calculated_in_step_2>,
     "timezone": "UTC"
   }
   ```

Write the script, save it to `/home/user/fix_restore.sh` (or `.py`, etc.), and execute it so that the `config.ini` is updated and the `restore_status.json` file is generated.