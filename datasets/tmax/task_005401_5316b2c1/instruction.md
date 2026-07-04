You are an AI assistant helping a data researcher organize a messy dataset environment. 

The researcher has an archive at `/home/user/dataset_archive.tar.gz`. This archive contains several data files, a multi-line log file named `transfer.log`, and some poorly formatted subdirectories that contain infinite symlink loops. 

Your task is to extract the archive, parse the log to find successfully transferred data files, filter out any paths that result in symlink loops or broken links, and securely log the valid files and back them up.

Here are your specific instructions:

1. **Extract the Archive**: Extract `/home/user/dataset_archive.tar.gz` into the directory `/home/user/dataset/`.
2. **Write a C Program**: Write a C program at `/home/user/parser.c` and compile it to `/home/user/parser`. The program must do the following:
   - Accept exactly three command-line arguments: the path to the log file (`/home/user/dataset/transfer.log`), the base dataset directory (`/home/user/dataset/`), and an output summary file (`/home/user/valid_files.txt`).
   - Read the multi-line log file. Each record in the log file has the following format (spanning multiple lines):
     ```
     ---RECORD---
     DatasetID: <integer>
     Status: <SUCCESS|FAILED>
     Path: <relative/path/to/file>
     ------------
     ```
   - For every record where `Status: SUCCESS`, extract the `Path`.
   - Resolve the absolute path of the file (Base directory + Path). You must safely handle paths that point into infinite symlink loops (e.g., using `stat()` which will safely fail on a loop, unlike naive recursive traversal).
   - If the file is a valid, existing regular file, append a line to the output summary file in the format: `<Path> <size_in_bytes>`.
   - **Crucial**: Because this C program is intended to be run by multiple parallel workers in the future, you **must** use POSIX file locking (`flock()` or `fcntl()`) to acquire an exclusive lock on the output summary file before writing each line, and release it afterward.
3. **Run the Program**: Execute your compiled C program with the appropriate arguments to generate `/home/user/valid_files.txt`.
4. **Create a Backup**: Based on the valid files identified in your summary text file, create a standard uncompressed tarball at `/home/user/clean_backup.tar` that contains *only* the valid `.dat` files. Store them at the root of the tarball (do not preserve the full `/home/user/dataset/` directory structure in the archive).

Ensure that your C program robustly handles the multi-line parsing and explicitly uses file locks.