You are acting as a capacity planner and system administrator. You need to build a custom resource monitoring system that triggers automatic backups and cleanup when directory capacity thresholds are met, managing it all via a custom service lifecycle script. 

Your task is to write and configure several components in `/home/user/`:

1. **The Target Directory**: 
   Create a directory `/home/user/app_data` and `/home/user/backups`.

2. **The Backup Script (`/home/user/backup.sh`)**:
   Write a robust bash script that:
   - Uses `set -e` to exit on errors.
   - Creates a compressed tarball of `/home/user/app_data` and saves it to `/home/user/backups/app_backup.tar.gz`.
   - After a successful tar command, deletes all files ending in `.dat` inside `/home/user/app_data`.
   - Appends the exact line `BACKUP_SUCCESS` to `/home/user/capacity.log`.
   - Ensure the script is executable.

3. **The C++ Capacity Monitor (`/home/user/monitor.cpp`)**:
   Write a C++ program that acts as a daemon. It must:
   - Loop indefinitely, checking the total size of all files in `/home/user/app_data` every 1 second.
   - If the total size of files in the directory strictly exceeds 10,000,000 bytes (10 MB):
     - Append the exact line `CAPACITY_WARNING: <size_in_bytes>` to `/home/user/capacity.log`.
     - Execute the bash script `/home/user/backup.sh` via the `system()` call or similar.
     - Append the exact line `RECOVERY_COMPLETE` to `/home/user/capacity.log`.
   - Compile this C++ file to an executable named `/home/user/monitor`.

4. **The Service Lifecycle Manager (`/home/user/service_manager.sh`)**:
   Write a bash script that accepts one argument (`start` or `stop`) to manage the compiled `/home/user/monitor` process.
   - `./service_manager.sh start`: Starts the `/home/user/monitor` in the background, saves its PID to `/home/user/monitor.pid`, and appends `SERVICE_STARTED` to `/home/user/capacity.log`.
   - `./service_manager.sh stop`: Reads the PID from `/home/user/monitor.pid`, kills the process, removes the PID file, and appends `SERVICE_STOPPED` to `/home/user/capacity.log`.

5. **The Staged Workload Simulator (`/home/user/workload.sh`)**:
   Write a script that creates files to test the system. It should loop 6 times. In each iteration:
   - Create a 2MB file named `data_<iteration>.dat` in `/home/user/app_data` (e.g., using `dd if=/dev/urandom of=/home/user/app_data/data_1.dat bs=1M count=2`).
   - Sleep for 1 second.

**Execution Steps to Complete the Task**:
1. Create all the above scripts and compile the C++ program.
2. Start the monitor using `./service_manager.sh start`.
3. Run the workload simulator `./workload.sh` and wait for it to finish.
4. Stop the monitor using `./service_manager.sh stop`.

When you are done, the file `/home/user/capacity.log` must exist and contain the sequence of events.