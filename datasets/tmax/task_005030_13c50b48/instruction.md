You are a storage administrator managing disk space on a backup server. We have a multi-service backup pipeline located in `/home/user/app/` that is currently failing. 

The pipeline consists of three components:
1. **Redis** (running on `127.0.0.1:6379`): Stores the status of backup jobs.
2. **Nginx** (running on `127.0.0.1:8080`): An authenticated gateway that receives HTTP backup requests and forwards them via raw TCP to our custom archiver daemon.
3. **Archiver Daemon** (C program expected to listen on `127.0.0.1:9000`): A custom service that processes backup requests.

Your task is to fix and finalize the Archiver Daemon. We have provided a skeleton in `/home/user/app/src/archiver.c`. 

Currently, the daemon has several fatal flaws:
- **Encoding mismatch:** It attempts to read the exclusion configuration file (`/home/user/app/config/excludes.conf`) as standard ASCII/UTF-8. However, this file is actually encoded in UTF-16LE. You must read this file, convert the contents to UTF-8, and parse the line-separated list of filenames to exclude.
- **Infinite Symlink Loops:** The recursive directory traversal logic blindly follows symlinks. The backup directories in `/home/user/data/` contain malicious or accidental symlink loops. You must implement cycle detection (e.g., tracking device and inode numbers) to skip symlinks that would cause a loop, while still following valid, non-cyclic symlinks.
- **Incomplete Archiving:** After computing the files, it needs to actually create an archive. For every file not excluded and not part of a symlink cycle, append its relative path and its exact byte size (format: `relative/path:size\n`) to a manifest file. Then, use the `tar` command via `system()` or `exec()` to create a gzip-compressed tarball (`.tar.gz`) containing only the valid, traversed files. 
- **Service Integration:** After successfully creating the archive at `/home/user/archives/<basename>.tar.gz` and the manifest at `/home/user/archives/<basename>.manifest`, the C daemon must connect to Redis at `127.0.0.1:6379` and execute the command `SET backup_status:<basename> COMPLETED`.

**Daemon Communication Protocol:**
The daemon should listen on TCP port 9000. Nginx will forward requests as a single plaintext line: `BACKUP <absolute_directory_path>\n`. 
Once the backup is complete and Redis is updated, the daemon must respond to the TCP client with `OK\n` and close the connection.

**Requirements:**
1. Install any necessary development libraries (e.g., `libhiredis-dev`, `iconv` libraries).
2. Write your code in C, modifying `/home/user/app/src/archiver.c`.
3. Compile the daemon to `/home/user/app/bin/archiver`.
4. Ensure Nginx and Redis are running, then start your daemon in the background.
5. Create a test log file at `/home/user/app/test_run.log` containing the exact manifest output of a test run on `/home/user/data/test_vol`.

Configure the system so that when an authenticated POST request is sent to Nginx, the end-to-end flow executes flawlessly. Nginx is configured to require the header `Authorization: Bearer disk-admin-token-99`.