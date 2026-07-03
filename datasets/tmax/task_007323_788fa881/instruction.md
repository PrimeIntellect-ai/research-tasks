You are a backup administrator responsible for archiving server logs. 

You have a directory `/home/user/raw_logs/` containing several `.log` files. Not all files need to be backed up, and not all contents of the files are relevant.

Your task is to implement an incremental, filtering backup system using standard Linux shell tools and a custom Rust archiver.

Here are the specific requirements:

1. **Incremental Backup Filter**: 
   The file `/home/user/last_run.txt` contains a UNIX epoch timestamp representing the last time a backup was run. You must only process `.log` files in `/home/user/raw_logs/` whose modification time (mtime) is strictly *greater* than this timestamp.

2. **Text Transformation**:
   For the files that qualify, we only want to archive lines that contain the exact string `"CRITICAL"`. You must use a standard command-line text transformation tool like `awk` or `sed` to filter these lines.

3. **Custom Rust Archiver**:
   Create a Rust Cargo project in `/home/user/archiver`.
   Write a Rust program that reads a list of absolute file paths from standard input (`stdin`), one per line.
   For each file path, your program should:
   - Execute the text transformation (`awk` or `sed`) as a child process to extract only the "CRITICAL" lines from that file.
   - Capture the standard output stream of this child process.
   - Compress this stream on the fly using Gzip (you may add the `flate2` crate to your dependencies).
   - Append the compressed data to a custom binary archive file at `/home/user/incremental.archive`.

4. **Custom Archive Format**:
   The `/home/user/incremental.archive` file must sequentially contain the following for each processed file:
   - `[Filename Length]`: A 16-bit unsigned integer (Little-Endian) representing the byte length of the *base* filename (e.g., `server_1.log`, NOT the full path).
   - `[Filename]`: The UTF-8 bytes of the base filename.
   - `[Compressed Data Size]`: A 32-bit unsigned integer (Little-Endian) representing the byte size of the Gzipped payload.
   - `[Compressed Data]`: The raw Gzipped bytes of the filtered log lines.

**Execution:**
You must provide a shell script at `/home/user/run_backup.sh` that pipelines the files needing backup (e.g., using `find`) into your compiled Rust archiver. Execute this script to generate `/home/user/incremental.archive`.

The final state will be evaluated by inspecting `/home/user/incremental.archive`.