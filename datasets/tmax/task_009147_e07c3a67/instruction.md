You are an artifact manager responsible for curating binary repositories. You have received an unverified incremental backup archive located at `/home/user/incoming_backup.tar.gz`. This archive contains compiled binaries, text files, and potentially dangerous symlink loops caused by a misconfigured backup script.

Your objective is to extract, parse, and clean this repository using Python.

Perform the following tasks:
1. Extract `/home/user/incoming_backup.tar.gz` to the directory `/home/user/repo`.
2. Write a Python script to scan the `/home/user/repo` directory. Your script must:
   - Identify all valid ELF binary files.
   - Gracefully handle and ignore any symlink loops or broken symlinks.
   - Parse the ELF header of each valid executable to determine its "Machine" type (e.g., using `readelf -h` or a Python library).
   - Resolve any valid symlinks to their ultimate targets to avoid processing the same underlying ELF file multiple times.
3. Generate a JSON catalog file at `/home/user/elf_catalog.json`. 
   - The JSON file must be a single dictionary.
   - The keys must be the absolute paths of the unique, resolved ELF files (e.g., `"/home/user/repo/bin1"`). Do not use symlink paths as keys.
   - The values must be the exact "Machine" string parsed from the ELF header (e.g., `"Advanced Micro Devices X86-64"`).
4. Create a clean, flat archive of the curated binaries at `/home/user/clean_artifacts.tar.gz`.
   - This archive must contain ONLY the unique, valid ELF files identified in step 2.
   - The files must be placed at the root level of the archive (no directories).
   - Symlinks, text files, and loops must NOT be included in this archive.

Ensure your Python script handles the symlink loop robustly without crashing or hanging.