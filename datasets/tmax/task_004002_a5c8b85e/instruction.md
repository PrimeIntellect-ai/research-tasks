You are a backup administrator responsible for optimizing our data archiving pipeline. Currently, we have a slow Python script (`/home/user/slow_backup.py`) that processes incoming files, but it's not scaling well.

Your task is to write a highly optimized C++ replacement for this script. 

Here is how the pipeline works:
1. We have a raw data directory at `/home/user/raw_data/` containing thousands of files.
2. The archiver must iterate through all files in this directory.
3. For each file, compute its SHA-256 checksum.
4. The file must be logically renamed (in the archive and manifest) to `<sha256>_<original_filename>`. (Do not modify the files in `/home/user/raw_data/` directly).
5. Generate a manifest mapping the new logical filename to the original filename and its SHA-256 checksum.
6. Create an uncompressed tarball named `/home/user/backup.tar` containing all the files under their new logical names.
7. Push the manifest as a JSON string to a local Redis server (running on `127.0.0.1:6379`) under the key `backup:manifest`. The JSON format must be:
   `{"<new_name>": {"original": "<original_filename>", "sha256": "<checksum>"}, ...}`

To test your implementation:
- A Redis instance is already running on port 6379.
- A validation service is running on port 8080. You can trigger validation by running `curl http://127.0.0.1:8080/validate`. It will check `/home/user/backup.tar` against the Redis key `backup:manifest`.

Constraints:
- You must write the solution in C++ (`/home/user/fast_backup.cpp`).
- You may use standard libraries, `libcrypto` (OpenSSL) for SHA-256, `libtar` or `libarchive` for tarring, and `hiredis` for Redis communication.
- The compiled executable must be placed at `/home/user/fast_backup`.
- Your C++ implementation must produce identically structured output to the Python script but must run significantly faster. An automated verifier will measure the execution time of `/home/user/fast_backup` and it must process 10,000 files in under 2.0 seconds.

Write your code, compile it, and ensure `curl http://127.0.0.1:8080/validate` returns `{"status": "success"}`.