You are a storage administrator tasked with managing a rapidly growing log directory. Our logging infrastructure relies on a few microservices, and disk space is critically low. 

Currently, there are two services running on this machine (managed via a multi-service setup in `/app/`):
1. **Redis**: Running on `127.0.0.1:6379`. It is used as a metadata store to track which files have been processed.
2. **Log API**: A local HTTP service running on `127.0.0.1:5000`. 

First, trigger the generation of the raw logs by making a `POST` request to `http://127.0.0.1:5000/generate`. This will populate `/home/user/raw_logs/` with hundreds of heavily nested directories containing `.log` files.

Your task is to write and execute a Bash script at `/home/user/archive_logs.sh` that performs the following operations:
1. **Recursive Directory Traversal**: Traverse `/home/user/raw_logs/` to find all `.log` files.
2. **State Checking**: For each `.log` file found, check the local Redis instance. If the key `processed:<absolute_path_to_file>` exists and equals `"1"`, skip the file. 
3. **Archiving & Aggressive Compression**: Take all unprocessed `.log` files and combine them into a single, highly compressed solid archive located at `/home/user/archives/master_archive.tar.xz` (or use `zstd` with maximum compression if you prefer, e.g., `master_archive.tar.zst`). The raw logs contain highly repetitive JSON data; you must utilize stream redirection and advanced compression flags to ensure maximum deduplication and minimal final file size. 
4. **State Updating**: For every file successfully added to the archive stream, update Redis by setting the key `processed:<absolute_path_to_file>` to `"1"`.
5. **Bulk Renaming**: Rename all the successfully processed `.log` files in place by appending `.done` to their filenames (e.g., `app_01.log` becomes `app_01.log.done`).

**Evaluation Requirements:**
- We will evaluate the total disk size of `/home/user/archives/`. To pass, the total size of your compressed archive must be strictly **less than 1,500,000 bytes (1.5 MB)**. (The raw logs will total ~100MB, but due to high redundancy, this threshold is easily achievable with strong solid compression like `xz -9` or `zstd -19`).
- Every `.done` file must have a corresponding `"1"` entry in Redis under its original `.log` absolute path.
- No unprocessed `.log` files should remain in `/home/user/raw_logs/` after your script completes.

Ensure `/home/user/archives/` exists before writing to it. You are free to install any standard compression utilities (like `xz-utils` or `zstd`) via `apt-get` if they are not already present.