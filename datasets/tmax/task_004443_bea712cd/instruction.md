You are assisting a researcher who needs to clean and organize a massive, messy dataset of sensor logs. 

The researcher has raw logs stored in `/home/user/dataset/raw/`. The directory contains many subdirectories with `.log.gz` files.
Each uncompressed log contains multiple multi-line records formatted like this:
```
BEGIN_RECORD
TIMESTAMP: 1700000000
SENSOR_ID: 42
... various other lines ...
END_RECORD
```

Some of these records contain corrupted or invalid state transitions that crash the researcher's legacy analysis pipeline. The legacy pipeline executable is provided at `/app/sensor_parser`. It is a stripped binary that takes a single file containing a single record as an argument. It exits with `0` if the record is valid, and returns a non-zero exit code (or crashes) if the record is invalid.

Your task is to write a C program at `/home/user/dataset_tool.c` and compile it to `/home/user/dataset_tool`.

The program must support two modes of operation:

**Mode 1: Verification**
Command: `./dataset_tool --verify <path_to_single_record_file>`
The program must read the single record from the file, analyze it, and exit with `0` if it is a "clean" record, or exit with `1` if it is a corrupted/invalid ("evil") record. You will need to reverse-engineer or black-box test `/app/sensor_parser` to deduce the exact logic of what makes a record invalid. 

**Mode 2: Concurrent Extraction and Assembly**
Command: `./dataset_tool --build <input_directory> <output_file>`
The program must:
1. Recursively traverse the `<input_directory>`.
2. Process all `.log.gz` files found (reading compressed streams directly using `zlib` or by piping from `zcat`/`gzip`).
3. Parse the multi-line records (split by `BEGIN_RECORD` and `END_RECORD`).
4. Filter out any invalid records using your deduced logic.
5. Append the valid records to `<output_file>`.
6. **Concurrency & Locking:** To speed up processing, your program must process multiple `.log.gz` files concurrently (using threads or `fork()`). Because multiple workers will be writing to the single `<output_file>` simultaneously, you **must** use POSIX file locking (`fcntl` or `flock`) to ensure that entire multi-line records are written atomically without interleaving lines from different records.

Compile your tool and run `./dataset_tool --build /home/user/dataset/raw /home/user/dataset/clean_combined.log` to process the existing dataset.

Ensure your code is robust, correctly manages file handles, properly synchronizes concurrent writes, and perfectly replicates the validation logic of the `/app/sensor_parser` binary.