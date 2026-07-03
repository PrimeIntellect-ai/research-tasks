You are a cloud architect migrating a local legacy application to a new cloud-ready structure on a Linux server. During the initial staging, the systemd worker service kept failing to start because it attempted to boot before the local database service was ready. You need to organize the new directory structure, backup the old application, fix the systemd configuration, and write a Python health check script to validate the migration.

Perform the following tasks:

1. **Backup Legacy State:**
   The old application is located at `/home/user/legacy_service`. 
   Create a gzip-compressed tar archive of this directory at `/home/user/archive/legacy_service.tar.gz`.

2. **Directory Structure & Links:**
   The new application resides in `/home/user/cloud_service`. All logs must be centralized.
   Create the directory `/home/user/shared_logs/cloud_service`.
   Inside `/home/user/cloud_service`, create a symbolic link named `logs` that points to the absolute path `/home/user/shared_logs/cloud_service`.

3. **Service Lifecycle Configuration:**
   There is a drafted systemd user unit file at `/home/user/services/cloud-worker.service`. 
   It currently fails in staging due to a missing dependency. Edit this file and add `After=cloud-db.service` and `Requires=cloud-db.service` under the `[Unit]` section to ensure it waits for the database service.

4. **Migration Validation Script:**
   Write a Python script at `/home/user/cloud_service/health_check.py` that programmatically verifies your migration steps. The script must perform the following checks:
   - Verify that the backup archive `/home/user/archive/legacy_service.tar.gz` exists and is a file.
   - Verify that `/home/user/cloud_service/logs` is a valid symbolic link pointing exactly to `/home/user/shared_logs/cloud_service`.
   - Read `/home/user/services/cloud-worker.service` and verify that both `After=cloud-db.service` and `Requires=cloud-db.service` are present in the text.
   
   If and only if all of these conditions are met, the script must write the exact string `MIGRATION_READY` to `/home/user/cloud_service/logs/status.log`. 

Once you have completed the setup and written the script, run `/usr/bin/env python3 /home/user/cloud_service/health_check.py` to generate the final status log.