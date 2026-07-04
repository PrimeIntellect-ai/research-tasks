You are a backup administrator for an advanced manufacturing firm. You need to process a disorganized, nested archive containing engineering assets for "Project Titan" before putting them into cold storage.

Your task is to organize, transform, and package this data into a standardized backup format. All your work should be done in `/home/user/`.

**Starting State:**
You have a primary nested archive located at `/home/user/backup_staging/titan_raw.tar.gz`.

**Phase 1: Extraction**
Extract `/home/user/backup_staging/titan_raw.tar.gz`. Inside, you will find:
- `config.json`: A metadata file containing asset IDs and their corresponding part names.
- `models.tar`: A tar archive containing raw GCode files.
- `firmware.zip`: A zip archive containing compiled ELF binaries.
Extract the contents of `models.tar` and `firmware.zip` as well.

**Phase 2: GCode Transformation**
1. Create a directory `/home/user/titan_processed/gcode/`.
2. Each extracted GCode file has a comment on its very first line in the format: `; AssetID: <ID>`
3. Read `config.json` to map each `<ID>` to its actual `name`.
4. Rename each GCode file to `<name>.gcode` (where `<name>` is the mapped name from the JSON) and move it to `/home/user/titan_processed/gcode/`. Spaces in names should be replaced with underscores (e.g., "Main Bracket" -> "Main_Bracket.gcode").

**Phase 3: ELF Manifest Generation**
1. Create a directory `/home/user/titan_processed/firmware/` and move all extracted ELF files there.
2. Generate a CSV manifest located at `/home/user/titan_processed/elf_manifest.csv`.
3. The CSV must have exactly this header: `Filename,Machine,SHA256`
4. For each ELF file, extract the "Machine:" field value using `readelf -h` (strip any leading/trailing whitespace), and calculate the file's SHA256 checksum.
5. Append a row for each ELF file to the CSV in the format: `filename.elf,Machine Value,sha256hash` (e.g., `controller.elf,Advanced Micro Devices X86-64,a1b2c3...`).

**Phase 4: Final Archiving and Checksums**
1. Create a final compressed archive `/home/user/titan_final.tar.gz` that contains the `titan_processed` directory and its contents. (The root of the tarball should be `titan_processed/`).
2. Generate a SHA256 checksum file `/home/user/titan_final.sha256` containing *only* the SHA256 hash of `titan_final.tar.gz` followed by two spaces and the filename `titan_final.tar.gz`.

Use Bash as your primary tool. You may create scripts or run commands directly in the terminal to accomplish this.