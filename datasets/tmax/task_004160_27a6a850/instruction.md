I am a researcher working on a dataset of 3D bioprinting logs. I received an archive named `/home/user/dataset.zip` from a collaborator, but my security scanner flagged it for a potential "Zip Slip" vulnerability (it contains files with paths trying to traverse outside the extraction directory, like `../`). 

I need you to safely process this dataset. Please write a Python script (or scripts) and use shell commands to perform the following operations:

1. **Safe Extraction**: Safely extract the contents of `/home/user/dataset.zip` into the directory `/home/user/extracted/`.
   - If an entry inside the zip file attempts to traverse out of the target directory (e.g., contains `../` or absolute paths pointing outside `/home/user/extracted/`), **skip** that file entirely.
   - Record the original path of every skipped malicious file in `/home/user/zip_warnings.log` (one path per line).

2. **GCode Processing**: The extracted archive contains several `.gcode` files (text files containing 3D printer trajectories).
   - Strip out all comments. A comment is any text starting with a semicolon `;` up to the end of the line. If the line becomes empty after removing the comment, remove the line entirely.
   - Split each cleaned `.gcode` file into smaller chunks of exactly 500 lines each (the final chunk may have fewer).
   - Name the chunks `<original_filename_without_extension>_part<N>.gcode`, where `<N>` is a 3-digit zero-padded number starting from `001` (e.g., `scaffold_part001.gcode`). Place these chunks in `/home/user/gcode_chunks/`.

3. **WAL Merging**: The archive also contains sensor write-ahead logs ending in `.wal` (binary files).
   - Merge all safely extracted `.wal` files into a single binary file located at `/home/user/merged_sensors.wal`.
   - The files must be concatenated in ascending alphabetical order based on their filenames.

4. **Summary Report**: Generate a final report at `/home/user/summary.txt` with exactly the following three lines (replace the brackets with the actual integer values):
   ```
   Blocked Files: [number of skipped zip slip entries]
   Total GCode Lines: [total number of clean GCode lines across all chunks]
   Merged WAL Size: [total size of merged_sensors.wal in bytes]
   ```