You are helping a researcher organize and back up their 3D printing dataset. They have a directory of files at `/home/user/research_data`, but their previous attempt at a backup script failed due to symlink loops, and it didn't handle their older file encodings or extract necessary metadata.

Your task is to write a Python script (or modify their approach) to perform a smart backup with the following requirements:

1. **Symlink Management:** The directory `/home/user/research_data` contains a symbolic link that points back to its own parent directory, creating an infinite loop. Your backup process must traverse the directory structure, but it must **ignore** all symbolic links to prevent infinite recursion. Do not include symlinks in the final archive.
2. **Character Encoding Conversion:** The dataset contains metadata files with a `.txt` extension. These were generated on an old system and are encoded in `ISO-8859-1`. When adding them to the backup, you must convert their contents to `UTF-8` encoding.
3. **GCode Parsing:** The dataset contains `.gcode` files. You need to parse each `.gcode` file to find the line that specifies the print time. The line always starts exactly with `; PRINT_TIME: ` followed by an integer representing the time in seconds (e.g., `; PRINT_TIME: 4500`). 
4. **Archiving:** Package all the processed files (with the original relative directory structure intact, e.g., `experiment1/meta.txt`) into a compressed tarball at `/home/user/safe_backup.tar.gz`.
5. **Metadata Logging:** Sum the print times from all the `.gcode` files you parsed. Write this total sum to a log file at `/home/user/gcode_time.log` in the exact format: `Total Print Time: <total_seconds>`.

Ensure all tasks are done using a Python script, which you should execute to produce the final `safe_backup.tar.gz` and `gcode_time.log`.