You are a container specialist tasked with building an automated recovery pipeline for a set of local microservices. The system uses a mock fstab file to track volume backups, and when a service crashes, its volume must be restored from an encrypted backup using a C++ orchestration tool.

Here are your instructions:

1. **Log Processing**: Look at `/home/user/microservices/service.log`. Find all services that have crashed. A crash line looks exactly like: `[ERROR] Service <service_name> crashed with code <X>`. Use shell text processing tools (like `grep`, `awk`, or `sed`) to extract just the names of the crashed services and save them, one per line, into `/home/user/microservices/crashed.txt`.

2. **Expect Scripting**: The backup extraction tool is an interactive script located at `/home/user/microservices/extract_backup.sh`. It takes two arguments: `<backup_file>` and `<destination_dir>`. When run, it prompts: `Enter password: `. Write an `expect` script at `/home/user/microservices/auto_extract.exp` that takes the same two arguments, runs the `extract_backup.sh` script, and automatically provides the password `secret_vault`.

3. **C++ Restoration Manager**: Write a C++ program at `/home/user/microservices/restore_manager.cpp`. This program must:
   - Read the list of crashed services from `/home/user/microservices/crashed.txt`.
   - Parse the custom fstab file at `/home/user/microservices/volumes.fstab`. Each line contains space-separated fields: `<service_name> <backup_file_path> <active_volume_path>`.
   - For each crashed service, look up its backup file and active volume path from the fstab file.
   - Use `system()` or `fork()/exec()` to execute your `auto_extract.exp` script with the corresponding backup file and active volume path.
   - After successfully triggering the extraction for a service, append a line to `/home/user/microservices/recovery.log` in this exact format: `RESTORED <service_name> TO <active_volume_path>`

4. **Execution**: Compile your C++ program to `/home/user/microservices/restore_manager` and run it. 

Ensure that by the end of your tasks, `/home/user/microservices/recovery.log` exists with the correct entries, and the corresponding active volume directories contain the recovered files. Do not modify the existing backup script or the fstab file.