You are a deployment engineer tasked with fixing a broken log rotation and backup system for a legacy Go application.

Recently, an automated log rotation cron job has been failing. It turns out the cron job was executing in an environment missing the correct `PATH`, causing the Go backup binary to either fail or write backups to the wrong directory. Furthermore, the Go binary's backup strategy was never fully implemented; it merely copies files without compressing them, causing the filesystem to fill up rapidly.

Your task is to complete the deployment workflow:

1. **Extract Specifications**: An image of the original deployment runbook is located at `/app/runbook_spec.png`. Use OCR (e.g., `tesseract`, which is pre-installed) to extract the text. From this image, you need to identify:
   - The required `CRON_SCHEDULE`
   - The `ENV_PATH` to be used in the cron job
   - The `BACKUP_DIR` destination

2. **Implement Log Rotation and Backup in Go**:
   - A skeleton file exists at `/home/user/log_manager/main.go`. 
   - Modify this Go program so that it reads the environment variables `ACTIVE_LOGS` and `BACKUP_DIR`.
   - The program must find all `.log` files in the directory specified by `ACTIVE_LOGS`.
   - It must package all found log files into a single `tar.gz` archive and save it to `<BACKUP_DIR>/backup.tar.gz`.
   - **Crucially**, to save filesystem space, you must implement maximum gzip compression (`gzip.BestCompression`). An automated verification step will measure the final file size of `backup.tar.gz` against a strict numerical threshold.
   - After successfully creating the archive, the program should delete the original `.log` files from `ACTIVE_LOGS` and append the line `HEALTH CHECK: OK` to `/home/user/health.log`.

3. **Deployment Script**:
   - Create an interactive bash script at `/home/user/deploy.sh` that performs the following:
     a. Compiles the Go program and outputs the binary to `/home/user/log_manager/bin/log_manager`.
     b. Creates the necessary target directories.
     c. Generates a crontab file at `/home/user/final_crontab.txt`. This file MUST explicitly define the `PATH` variable at the top (using the value extracted from the image), followed by the cron schedule, setting the `ACTIVE_LOGS` and `BACKUP_DIR` environment variables inline, and then calling the compiled Go binary.
     *(Format expectation for crontab: `PATH=<extracted_path>\n<extracted_cron> ACTIVE_LOGS=/home/user/active_logs BACKUP_DIR=<extracted_dir> /home/user/log_manager/bin/log_manager`)*

Make sure the Go code is robust, handles errors properly, and uses standard libraries (`archive/tar`, `compress/gzip`). Execute your `deploy.sh` script to set everything up and run the compiled Go binary at least once manually to prove it works.