You are an AI assistant helping a technical writer organize documentation and supplementary project files for an upcoming archive release.

You have been provided with a raw, disorganized archive at `/home/user/raw_assets.tar.gz`. It contains files with randomized alphanumeric names, no file extensions, and varying modification dates. The files include compiled binaries (ELF), 3D printing toolpaths (GCode), and database Write-Ahead Logs (SQLite WAL). 

Your task is to write a Bash script at `/home/user/organize_assets.sh` that performs the following steps:

1. **Extract** the contents of `/home/user/raw_assets.tar.gz` into `/home/user/processing/`.
2. **Filter by Metadata**: Identify only the files within the extracted contents that were modified **before** January 1, 2024. Ignore all files modified on or after this date.
3. **Analyze and Parse**: For each identified file, determine its true format by analyzing its contents/headers and extract specific metadata:
    *   **ELF Binaries**: Identify files that are ELF executables. Use the `file` command to determine the architecture (e.g., `x86-64`, `ARM`, `AArch64`).
    *   **GCode Files**: Identify text files containing GCode. You can identify them by searching for the exact string `; BEGIN GCODE` in the first 5 lines. Each GCode file will also have a line starting with `; ModelName: ` (e.g., `; ModelName: Bracket_v2`). Extract this model name.
    *   **SQLite WAL Files**: Identify SQLite 3 Write-Ahead Log files. These have the magic bytes `37 7f 06 82` or `37 7f 06 83` at the very beginning. (The `file` command typically recognizes these as "SQLite Write-Ahead Log").
4. **Bulk Rename and Organize**: Move the identified files into a new directory at `/home/user/organized_assets/` and rename them according to the following strict schema:
    *   ELF files: `binary_<architecture>_<original_filename>.elf` (e.g., `binary_x86-64_a1b2c3.elf`). Note: Ensure the architecture string doesn't contain spaces.
    *   GCode files: `gcode_<ModelName>.gcode` (e.g., `gcode_Bracket_v2.gcode`).
    *   WAL files: `database_<original_filename>.wal` (e.g., `database_f9e8d7.wal`).
5. **Archive**: Create a final ZIP archive of the organized directory at `/home/user/release_assets.zip`. The zip must contain the files directly at its root (do not include the `organized_assets` directory structure in the zip).

Make sure to install any required dependencies for zipping. Run your bash script to ensure `/home/user/release_assets.zip` is successfully generated.