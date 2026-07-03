You are acting as a backup administrator for a legacy manufacturing plant. The automated backup scripts have recently been failing because someone created recursive symlink loops in the primary data directories. Furthermore, the archival process requires specific format and encoding conversions to prepare the data for the new central storage system.

Your task is to write a script or set of commands to safely archive the machine data without falling into infinite loops. 

The source directory is `/home/user/machine_data`.
The destination directory for your final output is `/home/user/archive`. 
Make sure you create `/home/user/archive` before generating your outputs.

Requirements:
1. **Directory Traversal**: Traverse `/home/user/machine_data`. You must completely ignore any symlinks (do not follow them, do not include them in the backup). 
2. **GCode Files (`*.gcode`)**: These files contain legacy machine instructions and are currently encoded in Shift-JIS. You must read them, convert their encoding to UTF-8, and prepare them for archiving.
3. **Write-Ahead Logs (`*.wal`)**: These files currently store data as plain-text hexadecimal strings (e.g., `ff ff 00 1a...`, separated by spaces or newlines). You must:
   - Convert the hex text into raw binary data.
   - Apply a custom byte-level Run-Length Encoding (RLE) compression to the binary data. 
   - The RLE format must represent data as pairs of bytes: `[Count][Value]`. 
   - `Count` is a single unsigned byte representing the number of consecutive occurrences of `Value` (from 1 to 255). If a sequence exceeds 255, split it into multiple RLE pairs. 
   - Example: 300 bytes of `0xFF` becomes `[255][0xFF]` followed by `[45][0xFF]`.
4. **Archiving**: Bundle all the processed `.gcode` and `.wal` files into a single, uncompressed tar archive located at `/home/user/archive/safe_backup.tar`. The internal structure of the tar file should be flat (all files at the root of the archive), retaining their original base filenames but with the new processed contents.
5. **Manifest**: Create a log file at `/home/user/archive/manifest.txt`. For every file processed and added to the tarball, write a single line in the following CSV format:
   `[original_absolute_path_in_machine_data],[final_processed_size_in_bytes]`
   Sort the manifest alphabetically by the original absolute path.

Notes:
- You may use any combination of Python and standard Bash utilities.
- Do not hardcode the names of the files in `/home/user/machine_data`, as they may vary.