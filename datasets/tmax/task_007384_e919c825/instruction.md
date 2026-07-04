You are tasked with building a Bash-based configuration change tracker. In complex server environments, large configuration files are often modified incrementally. We need a script to take chunk-level snapshots of recently modified configuration files to track which specific parts of the files changed.

Write a Bash script at `/home/user/snapshot_configs.sh` that performs the following operations:

1. **Metadata-based File Search:**
   - Search the directory `/home/user/system/configs` (and all subdirectories) for all files ending in `.conf`.
   - Only process files that are strictly newer than the reference timestamp file located at `/home/user/system/baseline.stamp`.
   - Only process files that are standard regular files and have a file size greater than 0 bytes.

2. **Exclusion List:**
   - Read `/home/user/system/overrides.txt`. Each line contains an absolute path to a configuration file that must be EXCLUDED from the snapshot, even if it meets the search criteria. Ignore empty lines.

3. **File Splitting and Parsing (Chunking):**
   - For each valid, non-excluded `.conf` file found, split the file contents into exactly 50-byte chunks. (If the file size is not a multiple of 50, the last chunk will be smaller).
   - Compute the SHA-256 hash (`sha256sum`) of each chunk.

4. **Merging and Formatting:**
   - Aggregate the results into a specific format: `[absolute_filepath]:[chunk_index]:[sha256_hash]`
   - `chunk_index` starts at 0 for the first 50-byte chunk of a file.
   - Sort the final aggregated list alphabetically by the absolute filepath, and then numerically by the `chunk_index`.

5. **Atomic Write:**
   - To ensure no other processes read a partially generated snapshot, your script MUST write the final sorted output to a temporary file first (created securely), and then atomically move/rename it to the final destination: `/home/user/config_snapshot.log`.

Constraints:
- You must use ONLY standard Bash built-ins, coreutils (e.g., `find`, `split`, `sha256sum`, `sort`, `mv`, `mktemp`, `grep`), and standard CLI tools. Python, Perl, Node, or other scripting languages are strictly forbidden.
- The script should be executable.
- Run your script once it is created to generate `/home/user/config_snapshot.log`.