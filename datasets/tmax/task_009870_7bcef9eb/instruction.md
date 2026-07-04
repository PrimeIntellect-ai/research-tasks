I am a researcher organizing a collection of binary datasets. I received an archive `/home/user/dataset.tar` from an untrusted source, and I suspect it might contain malicious paths attempting a directory traversal attack (e.g., extracting to `../` or absolute paths like `/root`). 

Please help me safely extract and analyze this archive by doing the following:

1. First, create a symbolic link at `/home/user/latest_dataset` that points to `/home/user/dataset.tar`.
2. Write and execute a Python script `/home/user/process_dataset.py` that:
   - Reads the archive using the `/home/user/latest_dataset` symlink.
   - Creates the directory `/home/user/extracted_safe/` if it doesn't exist.
   - Extracts ONLY the safe regular files from the archive into `/home/user/extracted_safe/`. A file is considered "safe" if its archive path does NOT contain `..` and does NOT start with `/`. Ignore directories.
   - For each safely extracted file, reads the first 4 bytes (the binary header).
   - Formats the 4-byte header as an 8-character uppercase hexadecimal string (e.g., `DEADBEEF`).
3. Save the results to `/home/user/headers.txt`. Each line should contain the base filename (without directories) and its hex header, separated by a space. The lines must be sorted alphabetically by the filename.

Example line in `/home/user/headers.txt`:
`data_file.bin 89504E47`

Ensure that no unsafe files are extracted to the filesystem.