You are tasked with building an efficient configuration backup tool for our multi-service architecture. 

Our system consists of a Redis instance and a Python-based Configuration Management API. We have a test script that exercises this API by generating 1000 sequential configuration updates. These updates are logged in a multi-line format, and the raw config files are saved to disk. 

Your goal is to write a C++ program that acts as a differential backup archiver to save disk space.

### System Setup
1. First, start the services and the load generator by running: `/app/start_services.sh`. 
   This will start Redis on port 6379, the Config API on port 8080, and run a load generator that creates 1000 config versions.
2. The load generator writes to a log file at `/home/user/logs/config_updates.log`.
   The log records are multi-line and look like this:
   ```
   [BEGIN_UPDATE]
   TIMESTAMP: 1690000000
   TARGET_FILE: /home/user/history/app_v1.conf
   STATE: COMMITTED
   [END_UPDATE]
   ```
   *Note: Only records with `STATE: COMMITTED` should be backed up. Ignore `FAILED` or `ROLLBACK` states.*

### Your C++ Implementation
Write a C++ program at `/home/user/backup_tool.cpp` and compile it to `/home/user/backup_tool`.
When executed as `./backup_tool`, it must:
1. Parse `/home/user/logs/config_updates.log` to find all committed configuration files.
2. Create a single binary archive file at `/home/user/archive.bin`.
3. **Binary Header Requirement**: The first 10 bytes of `/home/user/archive.bin` MUST exactly be:
   - Magic bytes (4 bytes): `BCKP` (in ASCII)
   - Version (2 bytes, little-endian unsigned integer): `1`
   - Entry count (4 bytes, little-endian unsigned integer): The total number of backed up (committed) files.
4. **Differential Storage**: To conserve space, your archive must not store the full text of every configuration file. The base file (`app_v1.conf`) can be stored in full, but subsequent versions must only store the changed data (e.g., unified diffs, or compressed deltas). You are free to call external tools like `diff` via `popen` from your C++ code or implement a basic line-diff algorithm. 
5. The specific internal format of the payload (after the 10-byte header) is up to you, as long as it achieves the size reduction.

### Success Criteria
- The C++ program compiles and runs successfully.
- `/home/user/archive.bin` contains the exact 10-byte binary header specified above.
- **Metric Threshold**: Storing 1000 full configuration files would take approximately 4.5 MB. Your differential backup archive (`/home/user/archive.bin`) MUST be strictly **less than 250,000 bytes** in total size. 
- You do not need to implement the restore/extraction functionality for this task, only the archiving.