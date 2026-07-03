We have a background data-collection service that fails to behave correctly when run via our automated scheduler, though it seems to work fine when engineers run it manually. 

The service is triggered by `/home/user/trigger_worker.sh`, which executes the binary `/home/user/bin/service_worker`. When triggered by the scheduler, the environment is stripped. Because of this, the `APP_DIR` environment variable is missing, causing the worker to write its data logs directly into `/home/user/` instead of the designated `/home/user/app_data/` directory.

Your tasks are:
1. Modify `/home/user/trigger_worker.sh` so that it explicitly sets `APP_DIR=/home/user/app_data` and exports it before executing `/home/user/bin/service_worker`.
2. Write a monitoring script at `/home/user/monitor.sh` (make it executable) that performs the following actions:
   - Calculates the total disk space used by the `/home/user/app_data/` directory (in bytes).
   - If the size of the directory is strictly greater than 1024 bytes, it must:
     a) Find and kill the running `service_worker` process.
     b) Write the exact string `QUOTA EXCEEDED` to `/home/user/alert.log`.
   - If the size is 1024 bytes or less, it must write the exact string `OK` to `/home/user/alert.log`.

Ensure that you create the `/home/user/app_data` directory if it does not already exist. You do not need to start the service permanently; just ensure the scripts are correctly formulated so they work when our testing suite runs them.