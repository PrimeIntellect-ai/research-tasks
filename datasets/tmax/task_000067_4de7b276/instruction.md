You are a storage administrator managing a pool of manufacturing data. Your automated backup systems have been failing due to a user accidentally creating recursive symlink loops in their project directories. You need to write a script to safely parse, clean, and verify the storage pool without getting trapped in infinite directory loops.

Write a Python script at `/home/user/process_storage.py` that processes the directory `/home/user/storage_pool` and performs the following tasks:

1. **Recursive Traversal with Loop Prevention**: The script must traverse `/home/user/storage_pool`. There are symlink loops in this directory structure (e.g., a directory linking back to its parent). Your script must avoid infinite loops and process each unique file exactly once.

2. **Archive Integrity Verification**: 
   - Identify all files ending in `.tar.gz`.
   - Verify their integrity (i.e., ensure they are actually valid, uncorrupted gzip-compressed tar archives).
   - Keep a list of the absolute paths of any `.tar.gz` files that are corrupt or invalid.

3. **GCode Transformation**:
   - Identify all files ending in `.gcode`.
   - Read each file and remove all comments. In GCode, a comment begins with a semicolon (`;`) and continues to the end of the line.
   - If a line becomes completely empty or contains only whitespace after removing the comment, do not include it in the output.
   - Strip trailing whitespaces from remaining lines.
   - Save the cleaned GCode files into `/home/user/cleaned_gcode/` using their original filenames. (You can assume all original `.gcode` filenames are unique).

4. **Reporting**:
   - The script must generate a JSON report at `/home/user/storage_report.json` with the following structure:
     ```json
     {
       "processed_gcode_count": <integer>,
       "corrupt_archives": [
         "<absolute_path_1>",
         "<absolute_path_2>"
       ]
     }
     ```
   - The `corrupt_archives` list must contain the absolute paths to the corrupted `.tar.gz` files, sorted alphabetically.

Execute your script to ensure `/home/user/cleaned_gcode/` is populated and `/home/user/storage_report.json` is generated correctly.