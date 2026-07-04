You are a storage administrator tasked with managing disk space for a highly verbose application. The application generates massive log files and quickly consumes disk space. You need to implement an automated log rotation, chunking, and archiving pipeline, and expose the results via HTTP and a custom TCP API for the monitoring team.

A startup script located at `/app/start.sh` is already running in the background. It continuously writes log files to `/home/user/raw_logs/`. 
For each log file, the application writes data to `log_YYYYMMDD_HHMMSS.log`. Once it has finished writing to a specific log file, it creates an empty marker file named `log_YYYYMMDD_HHMMSS.done`.

Your objective is to write and run a system (using any language of your choice) that performs the following tasks:

1. **Watch and Process**: Continuously monitor `/home/user/raw_logs/` for new `.done` files.
2. **Split and Compress**: When a `.done` file appears, split the corresponding `.log` file into exactly 100 KB (102,400 bytes) chunks. Name the chunks systematically (e.g., `chunk_aa`, `chunk_ab`). 
3. **Archive**: Pack these chunks into a single zip archive named `archive_YYYYMMDD_HHMMSS.zip` (matching the timestamp of the log file) inside the directory `/home/user/archived_logs/`.
4. **Link Management**: Maintain a symbolic link at `/home/user/archived_logs/latest.zip` that always points to the most recently created archive.
5. **Cleanup**: Delete the original `.log` file, the `.done` file, and the intermediate chunk files to free up disk space.

You must also provide two network services for the monitoring team:
6. **HTTP File Server**: Serve the `/home/user/archived_logs/` directory over HTTP on port `8080`.
7. **TCP API Server**: Create a TCP server listening on port `9090`. 
   - When a client sends the string `LATEST\n`, the server must respond with the exact filename (just the basename, e.g., `archive_20240101_123456.zip\n`) that `latest.zip` currently points to.
   - When a client sends the string `COUNT\n`, the server must respond with the total number of `.zip` files currently present in `/home/user/archived_logs/` followed by a newline (e.g., `3\n`).

Keep your watcher and servers running in the background. Ensure the `/home/user/archived_logs/` directory exists before your script tries to write to it.