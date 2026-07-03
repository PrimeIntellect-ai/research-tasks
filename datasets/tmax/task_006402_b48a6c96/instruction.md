You are an AI assistant acting as a Storage Administrator. A server is running out of disk space due to a directory containing numerous application backup archives (`.tar.gz`). Many of these archives contain identical executable files (ELF binaries) and some archives are corrupted or represent failed backups.

Your task is to write a Go program `/home/user/workspace/dedup.go` and run it to deduplicate these backups. 

Here are the exact requirements for your program:

1. **Archive Processing & Integrity:**
   Iterate over all `.tar.gz` files in `/home/user/backups/`. Attempt to extract them to `/home/user/extracted/<archive_name_without_ext>/`. If an archive is corrupted and cannot be extracted cleanly, skip it and continue.

2. **Multi-line Log Parsing:**
   Inside each extracted archive, there is a `backup.log` file. Read this file. A valid backup log contains multi-line records formatted exactly like this:
   ```
   --- BACKUP START ---
   Timestamp: <some_date>
   Status: <STATUS_VALUE>
   Message: <some_message>
   --- BACKUP END ---
   ```
   Parse the log. If the log does not contain `Status: SUCCESS` within the `--- BACKUP START ---` and `--- BACKUP END ---` block, the backup is considered failed. You must skip further processing of failed backups (do not symlink their logs or deduplicate their binaries).

3. **Symlink Management:**
   For every successful backup, create a symbolic link in `/home/user/log_links/<archive_name_without_ext>_backup.log` that points to the absolute path of the extracted `backup.log` file.

4. **ELF Parsing and Hard Link Deduplication:**
   For every successful backup, recursively find all files in its extracted directory (excluding the log file).
   Determine if the file is an ELF binary. If it is, parse its ELF sections to extract the GNU Build ID (from the `.note.gnu.build-id` section).
   To save space, you must deduplicate these ELF binaries:
   - If this is the first time you've encountered a specific Build ID, copy the ELF file to `/home/user/elf_master/<build_id>.elf`.
   - Then, replace the file in the extracted backup directory with a hard link pointing to `/home/user/elf_master/<build_id>.elf`.
   - If you've already seen this Build ID in a previous backup, delete the newly extracted ELF and replace it with a hard link to the existing master copy in `/home/user/elf_master/<build_id>.elf`.

**Environment Setup:**
- You must create the directories `/home/user/workspace`, `/home/user/extracted`, `/home/user/elf_master`, and `/home/user/log_links` before running your program.
- Use Go as the primary language (standard library is sufficient for all of this, including `debug/elf`, `archive/tar`, `compress/gzip`, `os`, `path/filepath`). 
- Compile and run your Go program to complete the deduplication process. 

Once your Go program has finished running, simply exit. The automated test will verify the system state.