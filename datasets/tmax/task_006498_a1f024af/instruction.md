You are a storage administrator managing a 3D printer farm server. The server is running out of disk space due to massive amounts of raw GCode files. Your task is to process these files to save space, back up the originals, and prepare them for distributed processing.

Write a Python script (or a combination of bash and Python) to perform the following operations:

1. **Configuration Parsing:** Read the configuration file located at `/home/user/config.ini`. This file contains the following structure:
   ```ini
   [Storage]
   source_dir = /home/user/raw_gcode
   dest_dir = /home/user/processed_gcode
   backup_dir = /home/user/backup
   lines_per_chunk = <integer>
   ```

2. **Text Transformation & Filtering:** For every `.gcode` file in the `source_dir`:
   - Remove all comments. In GCode, a comment starts with a semicolon (`;`) and continues to the end of the line.
   - Strip leading and trailing whitespace from each line.
   - Completely remove any resulting empty lines.

3. **File Chunking:** Split the cleaned GCode commands into smaller chunk files, placing them in the `dest_dir`.
   - Each chunk must contain exactly `lines_per_chunk` lines, except for the last chunk, which may contain fewer.
   - The naming convention for the chunks must be: `<original_filename_without_extension>_part<X>.gcode`, where `<X>` is a 1-based integer (e.g., `model1_part1.gcode`, `model1_part2.gcode`).

4. **Archiving & Cleanup:** 
   - Create a compressed tarball of all the original, unmodified GCode files. Save this backup as `/home/user/backup/raw_archive.tar.gz`.
   - Ensure the tarball structure contains just the files (or the `raw_gcode` directory containing them).
   - After successfully verifying the backup is created, delete all `.gcode` files from the `source_dir` to free up disk space.

Make sure your script executes successfully and leaves the system in the exact state described above.