You are helping a developer organize and consolidate project log files. The system uses a rudimentary custom compression format to store text snippets and a configuration file to track which files need processing.

Your task is to write a bash script at `/home/user/process.sh` that performs the following actions:

1. **Configuration File Interpretation**: 
   Parse the file `/home/user/project_logs/sync.conf`. The configuration file has two key-value pairs (format `key=value`):
   - `target`: The absolute path where the consolidated log should be written.
   - `sources`: A comma-separated list of filenames (located in `/home/user/project_logs/`) that need to be processed.

2. **Custom Decompression**:
   For each file listed in the `sources` variable, read its contents and decompress it. The custom compression (`.cst`) format applies two operations in this order during compression:
   - Base64 encoding of the original string.
   - Reversing the entire Base64 string.
   You must reverse this process to recover the original plain text log entry.

3. **File Locking and Concurrent Access**:
   Multiple background jobs occasionally write to the target log file. To prevent data corruption, you must safely append the decompressed text of each file to the target file by using `flock` to acquire an exclusive lock on the target file before writing. Wait for the lock if necessary. You can lock a file descriptor associated with the target file. Add a newline character after each appended entry if the decompressed text doesn't end with one, ensuring each log entry is on its own line.

**Requirements**:
- The script must be written in Bash and located exactly at `/home/user/process.sh`.
- The script must make sure the output file is created if it does not exist.
- The output file must contain the decoded strings in the exact order they appear in the `sources` list.
- Make the script executable (`chmod +x /home/user/process.sh`).
- Execute the script once to generate the final consolidated log.

The environment contains the configuration file and the `.cst` files in `/home/user/project_logs/`.