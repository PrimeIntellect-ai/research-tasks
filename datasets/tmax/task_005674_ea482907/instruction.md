You are an AI assistant helping a data researcher process a batch of compressed datasets. The researcher has a set of raw data files that need to be validated and uncompressed based on a configuration file. 

The raw compressed datasets are located in `/home/user/raw_data/`. They are gzip-compressed files.
The configuration file is located at `/home/user/rules.conf`. It contains validation rules in the format `filename:expected_line_count` (one per line).

Your task is to write a C program named `/home/user/dataset_processor.c` and compile it to `/home/user/dataset_processor`. When executed, the program must do the following:
1. Read `/home/user/rules.conf` to understand the expected line count for each file.
2. For each file listed in the configuration, attempt to open and decompress the corresponding `.gz` file in `/home/user/raw_data/`. You should use the `zlib` library in C (`zlib.h`) for compressed stream processing.
3. Verify the integrity of the archive. If the file is corrupt or cannot be decompressed, treat it as invalid.
4. If it decompress successfully, count the number of newline characters (`\n`) in the uncompressed stream to determine the line count.
5. If the archive is valid AND the line count exactly matches the expected count from the config:
   - Save the fully uncompressed text to a new file in the directory `/home/user/processed/` with the `.gz` extension replaced by `.txt` (e.g., `a.gz` becomes `a.txt`).
   - Append the line `VALID: <filename>` to `/home/user/summary.log`.
6. If the archive is corrupt, fails to decompress, or the line count does NOT match the expected count:
   - Do not write the uncompressed file to the `processed` directory.
   - Append the line `INVALID: <filename>` to `/home/user/summary.log`.

Requirements:
- Ensure the `/home/user/processed/` directory exists or create it before writing files.
- You must write the solution in C.
- Compile your program linking the zlib library (e.g., `-lz`).
- Ensure `/home/user/summary.log` exactly matches the required output formats.

Execute your compiled program so the final files and logs are created.