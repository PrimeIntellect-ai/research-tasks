You are an artifact manager AI agent. We have a staging directory of build artifacts that need to be curated, processed, and archived. The artifacts are located at `/home/user/artifact_staging/`. 

During the build process, several files were generated with inconsistent encodings, and we need to extract metadata from compiled binaries before packaging them into our repository.

Write and execute a Python script to perform the following operations:

1. **Process Text Files (Encoding Conversion)**:
   - Find all `.txt` and `.gcode` files in the `/home/user/artifact_staging/` directory (including subdirectories).
   - Some of these files are encoded in `UTF-16LE` or `ISO-8859-1` instead of `UTF-8`.
   - Read each file, determine its current encoding (you may use heuristics, `chardet`, or try/except blocks), and convert the file contents to `UTF-8`. Overwrite the original files with the UTF-8 encoded versions.

2. **Parse Binary Metadata (ELF Domain-Specific Parsing)**:
   - Identify all ELF binaries in the staging directory (files starting with the magic bytes `7F 45 4C 46`).
   - Extract the Machine architecture type (`e_machine` field) from the ELF header. 
   - You can parse the ELF header manually in Python (bytes 18-19) or use a subprocess call to `readelf`.

3. **Generate a Manifest File**:
   - Create a manifest file at `/home/user/manifest.json`.
   - The JSON should be a dictionary where the keys are the relative file paths from `/home/user/artifact_staging/` (e.g., `bin/app_x86`).
   - The value for each file must be a dictionary containing:
     - `"sha256"`: The SHA-256 checksum of the file (after any encoding conversions).
     - `"file_type"`: `"elf"` if it's an ELF binary, `"text"` if it's a `.txt` or `.gcode` file, or `"unknown"` otherwise.
     - `"e_machine"`: If the file is an ELF binary, include the machine architecture as a hex string (e.g., `"0x3e"` for x86_64). If not an ELF, omit this key.

4. **Archive the Artifacts**:
   - Create a gzip-compressed tar archive of the processed directory and the manifest file.
   - The archive must be saved to `/home/user/release_archive.tar.gz`.
   - The archive should contain the directory `artifact_staging/` (with all its processed contents) and `manifest.json` at the root of the archive.

You may install any required Python packages using `pip`. Ensure all file paths in your script are absolute where appropriate.