You are an artifact manager tasked with curating a messy repository of binary and manufacturing artifacts. The incoming artifacts are stored at `/home/user/incoming_artifacts` and contain a mix of `.tar.gz` and `.zip` archives. Some of these archives are corrupt. The valid ones contain either compiled ELF binaries or GCode files for 3D printing.

Your goal is to write a Bash script at `/home/user/curate.sh` and execute it to categorize these archives based on their integrity and internal contents. 

Your script must perform the following operations:
1. **Directory Traversal:** Recursively search for all `.tar.gz` and `.zip` files in `/home/user/incoming_artifacts`.
2. **Integrity Verification:** Check the integrity of each archive (using `tar -tzf` for tarballs and `unzip -t` for zip files). 
   - If an archive is corrupt, move it to `/home/user/quarantine/`.
3. **Domain-Specific Parsing:** For valid archives, temporarily extract them to inspect their contents.
   - **ELF Files:** If the archive contains an ELF file (identifiable by the `.elf` extension or by inspecting the file headers, but for this task, assume they have no extension and are executable, or simply run `readelf -h` on extracted files to find them). Assume there is at most one ELF file or one GCode file per archive. Use `readelf -h` to extract the "Machine:" field. Replace any spaces in the machine name with underscores (e.g., `Advanced_Micro_Devices_X86-64`).
   - **GCode Files:** If the archive contains a `.gcode` file, read it to find a specific metadata comment line that exactly matches the format: `; filament_type = <TYPE>` (e.g., `; filament_type = PETG`). Extract the `<TYPE>`.
4. **Curation:** Move the original valid archive into a new directory structure under `/home/user/curated_artifacts/`.
   - For ELF archives: `/home/user/curated_artifacts/ELF/<Machine_Type_With_Underscores>/<original_filename>`
   - For GCode archives: `/home/user/curated_artifacts/GCode/<filament_type>/<original_filename>`
5. **Logging:** Append a record of each processed archive to a log file at `/home/user/curation.log`. The format must be exactly:
   `[<STATUS>] <filename> - <TYPE> - <METADATA>`
   - `<STATUS>` is either `VALID` or `CORRUPT`.
   - `<filename>` is the base name of the archive.
   - `<TYPE>` is `ELF`, `GCode`, or `UNKNOWN` (if corrupt).
   - `<METADATA>` is the Machine Type (with underscores) for ELF, the filament type for GCode, or `N/A` if corrupt.

Example log lines:
`[VALID] firmware.tar.gz - ELF - Advanced_Micro_Devices_X86-64`
`[VALID] bracket.zip - GCode - PETG`
`[CORRUPT] broken.tar.gz - UNKNOWN - N/A`

Ensure all destination directories (`quarantine`, `curated_artifacts` and its subdirectories) are created dynamically by your script if they do not exist. After writing `/home/user/curate.sh`, execute it so the final state is achieved.