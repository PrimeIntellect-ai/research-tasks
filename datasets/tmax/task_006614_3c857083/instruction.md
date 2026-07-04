You are a backup administrator tasked with archiving data based on a system log. You need to process a raw log file and extract specific archiving requests into a structured manifest for the backup system.

The log file is located at `/home/user/backup_data/system.log`. It contains various log levels, but you are only interested in lines containing the tag `[ARCHIVE_REQ]`. These lines have the following format:
`YYYY-MM-DD HH:MM:SS [ARCHIVE_REQ] <file_path> <size_in_hex>`

Your task is to:
1. Initialize a new Rust project called `archiver` in `/home/user/archiver`.
2. Write a Rust program in this project that reads `/home/user/backup_data/system.log` using efficient streaming I/O (e.g., `BufReader`) to avoid loading the entire file into memory at once.
3. For each line containing `[ARCHIVE_REQ]`, extract the `<file_path>` and the `<size_in_hex>`.
4. Convert the hexadecimal size (which starts with `0x`) into a base-10 decimal integer.
5. Write the extracted and transformed data into a new CSV file at `/home/user/archive_manifest.csv`. The output format for each extracted line must be exactly: `file_path,decimal_size`.
6. Compile and run your Rust program to generate the `archive_manifest.csv` file.

Ensure your Rust program handles the conversion accurately and outputs strictly to the requested CSV path.