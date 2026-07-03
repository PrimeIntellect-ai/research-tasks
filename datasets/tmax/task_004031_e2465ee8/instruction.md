You are helping a developer organize and salvage project files from a set of legacy backup archives. 

You have been provided with a directory containing several backup archives at `/home/user/raw_backups/`. Unfortunately, some of the archives were corrupted during a network transfer.

Your task is to perform the following operations using standard Bash commands and tools:

1. **Verify Archive Integrity:** Inspect all `.tar.gz` files in `/home/user/raw_backups/`. Identify which archives are completely valid and which are corrupted. Ignore and do not process the corrupted archives.

2. **Extract and Flatten Configs:** For all uncorrupted archives, locate any files ending with `config.json`. Extract them and place them into `/home/user/clean_configs/`. You must strip all leading directory paths so that the config files end up directly inside `/home/user/clean_configs/` (i.e., flattened). If there are filename collisions, you can overwrite them (though the backups are designed to have uniquely named configs).

3. **Process Compressed Streams:** The uncorrupted archives also contain compressed log files ending in `.log.gz`. Without permanently extracting the uncompressed logs to disk, process the compressed streams of these logs to find all lines containing the exact string `CRITICAL`. 
   - Append all matching lines from all valid archives into a single file at `/home/user/critical_errors.log`.
   - Once all matching lines are collected, sort the file alphabetically (`sort /home/user/critical_errors.log -o /home/user/critical_errors.log`) to ensure deterministic output.

4. **Re-archive:** Finally, create a new archive at `/home/user/consolidated_configs.tar.gz` containing ONLY the files inside `/home/user/clean_configs/` (do not include the `clean_configs` directory itself in the archive's root tree; the files should be at the root of the tarball).

Ensure all directories exist before you write to them. Do not process the corrupted `.tar.gz` files at all.