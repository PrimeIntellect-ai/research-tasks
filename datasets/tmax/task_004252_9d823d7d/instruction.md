You are a storage administrator tasked with freeing up disk space on a critical server. 

In `/home/user/old_records`, there is a deeply nested directory structure containing historical `.txt` and `.log` files. Over time, a rogue process polluted these files with highly repetitive, bloated debug lines that always begin with the exact string `[VERBOSE-DUMP]`.

Your goal is to write a Rust program that cleans these files, archives them, and cleans up the original directory to reclaim disk space.

Please complete the following steps:
1. Initialize a new Rust project at `/home/user/space_saver`.
2. Write a Rust program in this project that performs the following:
   - Recursively traverses the `/home/user/old_records` directory.
   - Modifies every `.txt` and `.log` file in-place by removing any line that starts exactly with `[VERBOSE-DUMP]`.
   - Keeps track of the total number of `[VERBOSE-DUMP]` lines removed across all files.
   - After cleaning the files, creates a gzip-compressed tarball of the entire `old_records` directory at `/home/user/old_records_archive.tar.gz`.
   - Deletes the original `/home/user/old_records` directory completely.
   - Writes a file at `/home/user/summary.txt` containing only a single integer: the total number of `[VERBOSE-DUMP]` lines removed.
3. Run your Rust program so that the final state of the system meets all the requirements above.

Ensure your Rust program handles the file I/O safely and accurately. You may use any standard utilities or external crates (like `flate2`, `tar`, `walkdir`) by adding them to your `Cargo.toml`, or you can invoke system commands from within your Rust code to handle the archiving step, but the traversal and text editing must be handled programmatically by your Rust code.