You are tasked with building a configuration manager for a 3D printer fleet that tracks changes to firmware and print jobs. 

You need to create a Python daemon that watches a specific "spool" directory for new files, parses domain-specific metadata out of them, archives them, and securely records the event in a Write-Ahead Log (WAL) format.

Here are the complete requirements:

1. **Environment Setup**:
   - The watcher should monitor `/home/user/spool` for newly created files.
   - Processed files must be archived into `/home/user/archive`.
   - Ensure both directories exist. You may install any Python libraries you need (e.g., `watchdog`, `pyelftools`) into your user environment.

2. **File Processing Logic**:
   Write a Python script at `/home/user/fleet_watcher.py` that continually watches `/home/user/spool`. When a new file is completely written to this directory, process it based on its extension:
   
   **For `.gcode` files**:
   - Read the file and parse the multi-line configuration header. 
   - The configuration block is guaranteed to be at the start of the file, bounded by lines containing exactly `; BEGIN CONFIG` and `; END CONFIG`.
   - Inside this block, lines are formatted as `; KEY: VALUE`. You need to extract the value for the key `MACHINE_TYPE`.
   - Example line: `; MACHINE_TYPE: Prusa_MK3S`

   **For `.elf` files (Firmware updates)**:
   - Parse the ELF header to extract the machine architecture.
   - You must extract the architecture string (e.g., `EM_ARM`, `EM_X86_64`, `EM_AVR`) from the ELF e_machine header field.

3. **Archiving & WAL Logging**:
   - Immediately after processing a file, compress the original file into a gzip-compressed tarball (`.tar.gz`) and save it to `/home/user/archive/<original_filename>.tar.gz`. 
   - Note: The tarball should contain the file directly, not the absolute directory structure.
   - After archiving, append an entry to the Write-Ahead Log located at `/home/user/config_wal.log`.
   - The WAL log must strictly follow this format for each entry:
     `[YYYY-MM-DD HH:MM:SS] | <filename> | <FILE_TYPE> | <METADATA>`
     - `<filename>` is just the name of the file (e.g., `job1.gcode`).
     - `<FILE_TYPE>` is either `GCODE` or `ELF`.
     - `<METADATA>` is the extracted `MACHINE_TYPE` for GCode, or the ELF architecture string for ELF files.
     - Example WAL line: `[2023-10-25 14:00:01] | job1.gcode | GCODE | Prusa_MK3S`
   - Finally, delete the original file from `/home/user/spool`.

4. **Execution**:
   Start your watcher script in the background. Once your watcher is running, create a file named `/home/user/ready.flag` to signal that it is ready to receive files. The evaluation system will drop test files into the spool directory and verify the archives and WAL file.

Do not stop the background process after creating `ready.flag`. Leave it running so it can process the injected files.