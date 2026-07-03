You are a technical writer who recently inherited a massive, disorganized archive of legacy documentation. The archive is located at `/home/user/legacy_docs`. 

These files have several issues:
1. They are encoded in `Windows-1252`, but your modern documentation system requires `UTF-8`.
2. They have poor naming conventions and are missing date context.
3. The archive is expected to grow to hundreds of gigabytes, so processing must be memory-efficient.

Your task is to create and run a Rust utility that automates the cleanup of this archive. 

Please perform the following steps:
1. Create a new Cargo project at `/home/user/doc_processor`.
2. Write a Rust program in this project that recursively searches `/home/user/legacy_docs` for all files ending in `.txt`.
3. For each `.txt` file found, the program must:
   - Read the file efficiently (using streaming/buffered I/O or memory mapping).
   - Convert the text from `Windows-1252` encoding to `UTF-8`.
   - Extract the file's Last Modified metadata timestamp.
   - Rename the file in-place (in its current directory) by prepending the Last Modified date in `YYYY-MM-DD_` format (in UTC). For example, `notes.txt` modified on January 5th, 2021 becomes `2021-01-05_notes.txt`.
   - Overwrite the file with the new UTF-8 contents.
4. The program must generate a log file at `/home/user/migration_log.csv` containing the mapping of processed files. The CSV must have no header, and each line should strictly follow the format: `<original_absolute_path>,<new_absolute_path>` (e.g., `/home/user/legacy_docs/notes.txt,/home/user/legacy_docs/2021-01-05_notes.txt`).
5. Run your Rust program to complete the transformation.

Note: You may use third-party crates (like `encoding_rs`, `walkdir`, or `memmap2`) by adding them to your `Cargo.toml`.