You are an AI assistant helping a technical writer organize documentation for an embedded systems project. Automated builds drop various artifact files into a directory, and the writer needs a script to safely extract metadata from these files to generate an automated documentation index. 

The artifacts are located in `/home/user/artifacts/` and contain:
1. `firmware.elf`: A compiled ELF binary.
2. `jig_path.gcode`: A GCode file used by the automated testing rig.
3. `build_logs.tar.gz`: A compressed archive containing build logs.

Write a script (or a combination of scripts, e.g., Bash orchestrating Python or awk) that extracts specific metadata from these files and appends the results to a summary file at `/home/user/doc_index.txt`. 

Your solution MUST meet the following requirements:
1. **ELF Header Extraction:** Extract the "Entry point address" from `/home/user/artifacts/firmware.elf`.
2. **GCode Parsing:** Parse `/home/user/artifacts/jig_path.gcode` to find the maximum Z-height. Look for lines that contain `Z` followed by a number (e.g., `G1 X10 Y10 Z15.5`). Find the maximum numerical value associated with `Z`.
3. **Compressed Stream & Multi-line Parsing:** Process `/home/user/artifacts/build_logs.tar.gz` *without extracting it to disk*. Stream the contents to find a multi-line error block inside the compressed logs. The block starts with a line containing exactly `--- BEGIN FATAL ---` and ends with a line containing exactly `--- END FATAL ---`. Extract the text between these markers (excluding the markers themselves). Strip all newline characters from the extracted text so it becomes a single string.
4. **Safe Concurrency:** The technical writer's CI system might run your script concurrently. You must use file locking (e.g., `flock`) when writing to `/home/user/doc_index.txt` to prevent race conditions.

Format the output appended to `/home/user/doc_index.txt` exactly as follows (replace the bracketed placeholders with your extracted values):
```
ELF_ENTRY: [entry_point_address]
MAX_Z: [max_z_value]
FATAL_ERROR: [single_line_error_text]
```

Example output format:
```
ELF_ENTRY: 0x4000ab
MAX_Z: 42.5
FATAL_ERROR: Null pointer exception at main.c:42 Core dumped.
```

Create and run your script to generate the final `/home/user/doc_index.txt` file.