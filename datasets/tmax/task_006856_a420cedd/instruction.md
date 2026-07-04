I have a project backup archive located at `/home/user/project_backups.tar.gz`. This archive contains a mix of source code files, logs, `.gcode` files, and compiled ELF binaries. Due to an oversight, it also contains a nested archive named `inner_backup.tar` which has even more project files inside it.

I need you to organize this mess by extracting the files, analyzing the binaries, and creating a clean, filtered archive.

Please perform the following steps:
1. Extract `/home/user/project_backups.tar.gz` into a new directory `/home/user/extracted_project`.
2. Find `inner_backup.tar` within that extracted structure and extract its contents into the exact same directory where `inner_backup.tar` is located.
3. Recursively search through `/home/user/extracted_project` to identify all valid ELF files.
4. For every ELF file found, parse its ELF header to determine the machine architecture. Create a report at `/home/user/elf_report.txt`. Each line must be formatted exactly as:
   `[relative_path_from_extracted_project] - [Machine_Architecture]`
   (Example: `bin/tool1 - Advanced Micro Devices X86-64`)
   Use `readelf -h` to extract the "Machine:" field value exactly as it appears (trimming leading spaces). Sort the final `elf_report.txt` alphabetically by the file path.
5. Create a new, cleanly organized archive at `/home/user/filtered_backup.tar.gz` that contains *only* the ELF files and `.gcode` files from `/home/user/extracted_project`. The internal structure of this new tarball should be relative to `/home/user/extracted_project` (e.g., `tar -czf /home/user/filtered_backup.tar.gz -C /home/user/extracted_project ...`).

Make sure your commands correctly handle standard stream redirection and that you successfully parse the ELF headers.