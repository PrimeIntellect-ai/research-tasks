You need to help me organize a messy directory of project files containing compiled firmware binaries (ELF files), 3D printing toolpaths (GCode files), and some miscellaneous garbage files.

I need you to write and execute a Python script at `/home/user/organize.py` that processes the directory `/home/user/project_files` and organizes the recognized files into `/home/user/organized_files` using symbolic links, then generates a checksum manifest using atomic writes.

Here are the exact requirements for your script:

1. **Scan and Identify:**
   Recursively scan `/home/user/project_files/`.
   - **ELF Files:** Identify these by checking if the first 4 bytes of the file are the ELF magic number: `\x7fELF` (Hex: `7F 45 4C 46`).
   - **GCode Files:** Identify these by checking if the file ends with the `.gcode` extension AND the very first character of the file is either a semicolon (`;`) or the letter `G`.
   - Ignore all other files.

2. **Calculate Checksums:**
   For every identified ELF and GCode file, calculate its full SHA256 checksum.

3. **Create Symbolic Links:**
   Create the target directories `/home/user/organized_files/elf` and `/home/user/organized_files/gcode` if they don't exist.
   For each identified file, create a symbolic link in the appropriate category directory pointing to the original file's absolute path.
   The name of the symbolic link must be: `<original_filename>_<first_8_chars_of_sha256>` (e.g., if the original is `firmware.bin` and the sha256 starts with `a1b2c3d4`, the link is `firmware.bin_a1b2c3d4`). Preserve the original extension if it had one.

4. **Generate the Manifest (Atomic Write):**
   Create a JSON manifest tracking these files. The JSON should be a dictionary where the keys are the *absolute paths of the symbolic links created*, and the values are dictionaries with two keys:
   - `original_path`: The absolute path to the original file.
   - `checksum`: The full SHA256 checksum string.
   
   To prevent corruption if the script crashes, you MUST write this JSON data atomically to `/home/user/organized_files/manifest.json`. Write the data to `/home/user/organized_files/manifest.json.tmp` first, ensure it is flushed/synced, and then rename it to `manifest.json`.

After writing the script, execute it so that the `/home/user/organized_files/` directory is populated and the `manifest.json` is created.