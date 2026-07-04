You are a backup administrator tasked with archiving an old embedded manufacturing project. The project files are located in `/home/user/project_data` and contain a mix of different file formats scattered across a nested directory structure.

To prepare these files for the cold-storage archive, you need to write a Python script at `/home/user/archiver.py` that recursively scans the `/home/user/project_data` directory, parses specific domain formats to extract backup metadata, applies a custom compression routine to text assets, and outputs a final report.

Your script must perform the following actions:
1. **Recursive Traversal:** Find all files with `.elf` and `.gcode` extensions within `/home/user/project_data` and its subdirectories.
2. **Domain Parsing - ELF (`.elf`):** Parse the ELF headers to extract the Entry Point Address. You may use Python's built-in `struct` module or install a library like `pyelftools`. Record the entry point as a hex string (e.g., `"0x400080"`).
3. **Domain Parsing - GCode (`.gcode`):** Parse the GCode files to calculate the total extrusion. Find all lines starting with `G1` that contain an `E` parameter (e.g., `G1 X10 Y10 E2.5`). Sum all the `E` values found in the file. Round the total to 2 decimal places.
4. **Custom Compression:** For each `.gcode` file, create a custom compressed version in the same directory with the extension `.gcode.cz`. The custom compression algorithm must do the following:
   - Read the original text file.
   - Replace every occurrence of the string `"G0 "` with the byte `\x01`.
   - Replace every occurrence of the string `"G1 "` with the byte `\x02`.
   - Write the resulting byte sequence to the `.cz` file, prepended with the magic header bytes `CZMA` (in ASCII).
5. **Reporting:** Generate a JSON file at `/home/user/backup_report.json` containing a list of objects for all processed files. The list should be sorted alphabetically by the relative file path. Each object must have the following schema:
   ```json
   {
     "file": "relative/path/to/file.ext",
     "type": "elf" or "gcode",
     "metadata": {
       "entry_point": "0x..." // only for ELF
       "total_extrusion": 12.34 // only for GCode
     }
   }
   ```

Requirements:
- Ensure the script is fully self-contained or explicitly installs required dependencies via `pip` within the script or using a bash wrapper.
- Execute the script so that `/home/user/backup_report.json` is generated.
- Ensure the compressed `.cz` files are created alongside the original `.gcode` files.