You are tasked with organizing a chaotic collection of legacy log files for a development team. The team has a directory of gzipped log files scattered across various subdirectories. You need to write a Rust tool that concurrently processes these archives, parses their metadata, and reorganizes them into a clean structure using hard links and symlinks, while maintaining a thread-safe manifest.

Here are the specific requirements:

1. **Input Data**: 
   The raw log files are located in `/home/user/raw_logs/`. They are all `.gz` files. Inside each compressed file, the very first line is a JSON object containing metadata, specifically an `"app_id"` (string) and a `"timestamp"` (integer, representing a UNIX epoch).

2. **Rust Project Setup**:
   Create a new Rust project named `log_organizer` in `/home/user/log_organizer`. You may use standard crates like `flate2`, `serde`, `serde_json`, `rayon`, or `fs2` (or `fd-lock`). 

3. **Processing Logic**:
   Your Rust program must discover all `.gz` files in `/home/user/raw_logs/` (and its subdirectories) and process them **concurrently**.
   For each file, your program must:
   - Stream the uncompressed contents (without extracting the whole file to disk) just enough to read the first line.
   - Parse the JSON to extract `"app_id"` and `"timestamp"`.
   - Create the target directory `/home/user/organized_logs/<app_id>/` if it does not exist.
   - Create a **hard link** of the original `.gz` file into the target directory. The new hard link must be named `<timestamp>_<original_filename>`. 
     *(Example: If the original file is `server1_error.gz` and the timestamp is `1690000000`, the hard link should be `/home/user/organized_logs/backend_api/1690000000_server1_error.gz`)*.
   - Append a line to a central manifest file at `/home/user/organized_logs/manifest.log` in the format: `LINKED <original_filename> TO <app_id>`. Because multiple threads are processing files concurrently, you **must use file locking** (e.g., exclusive OS-level locks) when appending to this manifest file to prevent data corruption or interleaved writes.

4. **Symlinking the Latest Logs**:
   After all files are processed and hard-linked, your program must identify the file with the highest timestamp for *each* `app_id`.
   For each `app_id`, create a **symbolic link** at `/home/user/organized_logs/<app_id>/latest.gz` that points to the hard link with the highest timestamp.

5. **Execution**:
   Compile your Rust program using `cargo build --release` and run it so that the final state of `/home/user/organized_logs/` reflects all the requirements above.

Ensure your code is robust, handles errors gracefully, and strictly adheres to the paths and formats specified.