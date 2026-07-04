You are a storage administrator managing disk space and incoming backup files for a custom internal application. We have been receiving malicious and corrupted backup files, and we need a robust C++ filter to sanitize incoming data before it is ingested by our storage backend.

Our system comprises three user-space services:
1. `upload_api` (Flask, port 8080): Receives backup uploads and dumps them into `/home/user/uploads/`.
2. `redis-server` (port 6379): Tracks the number of successfully verified backups.
3. `stats_api` (Flask, port 8081): Reads the count from Redis and reports it.

Your tasks are as follows:

1. **System Configuration (Multi-Service)**
   The startup script `/home/user/start_services.sh` brings up these services, but they are currently failing or misconfigured. 
   - Fix the configuration file `/home/user/config/upload_config.json` so `upload_api` uses `/home/user/uploads/` as its upload directory.
   - Fix `/home/user/config/stats_config.json` to point to the correct Redis port (6379).
   - Ensure all three services are running.

2. **C++ Sanitizer Development**
   Write a C++ program at `/home/user/cbf_filter.cpp` and compile it to `/home/user/cbf_filter`. This tool must process our Custom Backup Format (CBF) files.
   
   CLI Signature: 
   `/home/user/cbf_filter <config_path> <input_dir> <output_dir>`
   
   **Requirements:**
   - **Recursive Traversal:** It must recursively scan `<input_dir>` for files.
   - **Configuration Parsing:** Read the JSON configuration at `<config_path>` (e.g., `/home/user/config/filter_config.json`). It contains `allowed_versions` (an array of integers) and `max_payload_size` (integer). You may use a simple manual parser or standard C++ tools.
   - **Binary Format Extraction:** Each file must be parsed according to the CBF spec:
     - Offset 0 (4 bytes): Magic bytes `0x42 0x4B 0x55 0x50` ("BKUP")
     - Offset 4 (2 bytes, Little Endian): Version number. Must be in `allowed_versions`.
     - Offset 6 (2 bytes, Little Endian): Flags (ignore for verification).
     - Offset 8 (4 bytes, Little Endian): Payload Size (`N`). Must be <= `max_payload_size`.
     - Offset 12 (`N` bytes): Payload data.
     - Offset 12 + `N` (4 bytes, Little Endian): Expected CRC32 checksum of the Payload data only.
   - **Verification:** Calculate the CRC32 of the payload (you can implement standard CRC32 or use zlib if installed). A file is valid ONLY IF the magic bytes match, the version is allowed, the size is within limits, the file size matches the expected layout exactly (12 + N + 4 bytes), and the CRC32 is correct.
   - **Bulk Renaming / Output:** For every valid file, write it to `<output_dir>` with the same base name, but append `.verified` (e.g., `backup1.dat` -> `<output_dir>/backup1.dat.verified`). Invalid files must be ignored (dropped). Do not recreate the directory structure in `<output_dir>`, just place all valid files flatly inside it. If there are name collisions, you can overwrite.

3. **End-to-End Flow**
   Write a shell script `/home/user/process_backups.sh` that:
   - Runs `./cbf_filter /home/user/config/filter_config.json /home/user/uploads /home/user/verified_backups`
   - Counts the number of `.verified` files in `/home/user/verified_backups`.
   - Updates the Redis key `verified_backup_count` with this integer count using `redis-cli`.

Test your setup thoroughly. We have provided sample files in `/home/user/sample_data/`. 
The automated verification will run your `cbf_filter` against an adversarial corpus of "evil" and "clean" files to ensure perfect accuracy.