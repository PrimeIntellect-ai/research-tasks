You are an artifact manager responsible for curating a repository of compiled binaries. You have received a batch of incoming files in `/home/user/incoming_artifacts`, which contains a mix of valid ELF binaries, text files, and corrupted data. 

Your objective is to build an automated curation pipeline in Bash that processes these files, organizes them into a structured repository, generates a summary report, and performs an incremental backup.

Complete the following steps:

1. **Parse and Filter**: Inspect all files in `/home/user/incoming_artifacts`. Identify the valid ELF files. You may use standard tools like `readelf`.
2. **Curate and Link**: For every valid ELF file, determine its Machine architecture (e.g., "Advanced Micro Devices X86-64") and its Type (e.g., "EXEC" for Executable file, "DYN" for Shared object file). 
   - Map the Machine architecture string to a folder-friendly name by replacing spaces with underscores and removing hyphens (e.g., "Advanced_Micro_Devices_X8664").
   - Map the Type to either "executable" (for EXEC) or "shared" (for DYN). 
   - Recreate the curated repository structure in `/home/user/curated_repo/<architecture_name>/<type>/`.
   - **Hard link** (do not copy) the valid ELF files from the incoming directory into their respective directories in `/home/user/curated_repo/` keeping their original filenames.
3. **Report Generation**: Generate a text report at `/home/user/artifact_report.txt`. Use tools like `awk` or `sed` to format the report. The report must contain exactly one line per architecture found, sorted alphabetically by architecture name. The format must be exactly:
   `[Architecture_Name] -> Executables: [Count], Shared: [Count]`
4. **Incremental Backup**: An initial snapshot file exists at `/home/user/backups/repo.snar` along with a base backup at `/home/user/backups/base.tar` (which captured an empty repository). Create an incremental backup of the `/home/user/curated_repo/` directory using GNU `tar`'s `--listed-incremental` feature. Use the existing snapshot file and save the new incremental archive to `/home/user/backups/inc.tar`.

Ensure your bash commands correctly handle the extraction of metadata and the generation of hard links. Do not copy the files, as disk space is strictly limited.