You are assisting a researcher in organizing a large, messy dataset of custom binary logs. The dataset directory is located at `/home/user/dataset`. 

Unfortunately, previous backup and organization scripts created several relative symlinks inside the dataset directory, some of which point back to parent directories, creating infinite loops.

Your task is to write a Rust program that traverses this dataset directory, parses specific custom log files, and produces a summary, while safely avoiding infinite symlink loops.

**System Details:**
1. **Configuration File**: There is a configuration file at `/home/user/config.ini`. It specifies the extension of the files you need to process and the 4-byte "magic signature" that denotes the start of a valid record.
   Format:
   ```
   [dataset]
   extension=wal
   magic=DEADBEEF
   ```
   (The magic signature is given in hex, representing the bytes `0xDE 0xAD 0xBE 0xEF`).

2. **File Format (WAL)**: The files to process (e.g., `.wal` files) are binary files containing a stream of records. Each valid record is exactly 16 bytes long:
   - The first 4 bytes are the magic signature (matching the config file, big-endian).
   - The remaining 12 bytes are arbitrary data payload.
   Note: Some files may contain corrupted data or garbage bytes between valid records. Your Rust program must scan through the file stream, identify the magic signature, read the 16-byte record (to skip its payload), and count how many valid records exist in the file. Use streaming/buffered I/O as some of the real files are too large to fit in memory.

3. **Symlink Trap**: The dataset directory contains symlinks. You must follow symlinks to find files, but you MUST implement cycle detection to prevent infinite recursion (e.g., if a symlink inside a subdirectory points back to `/home/user/dataset`).

**Your objective:**
Write a Rust project in `/home/user/wal_parser` to perform this task. 
The program must recursively scan `/home/user/dataset`, process every file matching the configured extension, count the valid records in each file, and write the results to `/home/user/wal_summary.txt`.

The output file `/home/user/wal_summary.txt` must contain exactly one line per processed file, in the format:
`[absolute_path_to_file]: [count]`

The lines must be sorted alphabetically by the absolute file path. 
For example:
```
/home/user/dataset/a.wal: 3
/home/user/dataset/subfolder/b.wal: 5
```

Build and run your Rust program to generate the `/home/user/wal_summary.txt` file.