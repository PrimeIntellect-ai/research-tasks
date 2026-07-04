As a cloud architect migrating legacy services to a new VPC, you need to automate the generation of network routing and storage mount configurations for services that have completed their migration. 

Your task is to create a Rust utility that processes migration status files, generates a shell script with network routing commands, updates a local fstab file, and schedules itself to run automatically.

Here are the requirements:

1. Create a Rust Cargo project named `migrator` in `/home/user/migrator`.
2. The Rust program must read a JSON file located at `/home/user/migration_data/legacy_services.json`. The JSON is an array of objects with the following format:
   `[{"service_name": "db-main", "ip_address": "10.5.1.100", "status": "migrated", "nfs_export": "10.10.10.50:/vol/db-main"}]`
3. The Rust program must filter for services where `"status"` is exactly `"migrated"`.
4. For each migrated service, the program must:
   a. Append a routing command to `/home/user/output/apply_routes.sh` in this exact format: 
      `ip route add <ip_address>/32 via 10.99.0.1` (where 10.99.0.1 is the new VPC gateway).
   b. Append a line to `/home/user/output/mock_fstab` in this exact format:
      `<nfs_export> /home/user/mnt/<service_name> nfs defaults,user,noauto 0 0`
5. The Rust program must ensure `/home/user/output/apply_routes.sh` starts with `#!/bin/bash` (only written once) and is marked as executable. If the files already exist, the program should overwrite them with fresh data based on the JSON.
6. Compile the Rust program in release mode.
7. Set up a user cron job that runs the compiled binary (`/home/user/migrator/target/release/migrator`) exactly every 5 minutes.
8. Once the cron job is set, save the output of your user's crontab (`crontab -l`) to `/home/user/output/crontab_dump.txt`.
9. Run your Rust binary once manually to ensure the output files are generated for verification.

Ensure that the output directory `/home/user/output/` exists before running your program. Do not execute the generated `apply_routes.sh` script, as you do not have root privileges to modify the actual system routing table.