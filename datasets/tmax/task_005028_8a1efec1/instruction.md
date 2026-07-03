You are a storage administrator managing a large, rapidly growing disk volume. You need a highly efficient tool to scan directories for large files and consolidate the findings into a single report. Because the storage volume is vast, the tool must scan concurrently, write safely to a shared log, and ensure the final report is updated atomically to prevent monitoring tools from reading partial data.

Your task is to write a C program named `/home/user/disk_nav.c` that fulfills these requirements, compile it to `/home/user/disk_nav`, and run it against a provided directory.

**Requirements for `disk_nav.c`:**
1. **Command Line Arguments:** The program should accept exactly three arguments: `./disk_nav <target_dir> <output_file> <min_size_bytes>`.
2. **Temporary File & Atomic Write:** The program must initially open a temporary file in the same directory as `<output_file>` (e.g., using `mkstemp`). After the entire scan is completely finished and all workers have exited, the parent process must atomically move/rename this temporary file to `<output_file>`.
3. **Recursive Directory Traversal & Concurrency:** 
    * The program must read the top-level contents of `<target_dir>`.
    * For *every* subdirectory found directly inside `<target_dir>`, the program must spawn a new child process (using `fork()`) to recursively traverse that subdirectory.
    * The parent process should handle scanning any regular files located directly in `<target_dir>`, and then `wait()` for all child processes to finish.
4. **File Locking:** When a process (parent or child) finds a regular file with a size greater than or equal to `<min_size_bytes>`, it must write the file's information to the shared temporary file. To prevent interleaved/corrupted writes from concurrent processes, every write to the shared file MUST be protected by an exclusive file lock (using `fcntl()` or `flock()`).
5. **Output Format:** Each logged file must be written to the log as a single line in the exact format:
   `<size_in_bytes> <absolute_file_path>\n`

**Actions to Perform:**
1. Create the C source code at `/home/user/disk_nav.c`.
2. Compile it using: `gcc -O2 -Wall /home/user/disk_nav.c -o /home/user/disk_nav`
3. Before running your program, you must create a test directory structure to verify your tool works. Create the following structure:
   - `/home/user/storage_root/`
   - `/home/user/storage_root/file_A.dat` (size: 2000 bytes)
   - `/home/user/storage_root/dir1/file_B.dat` (size: 5000 bytes)
   - `/home/user/storage_root/dir1/file_C.dat` (size: 100 bytes)
   - `/home/user/storage_root/dir2/sub/file_D.dat` (size: 8000 bytes)
   *(You can use `dd` or `head` to create files of exact sizes).*
4. Run your compiled program: 
   `./disk_nav /home/user/storage_root /home/user/large_files_report.txt 3000`

Ensure your program handles error checking gracefully (e.g., skipping unreadable files, handling fork failures). You are free to write helper bash scripts if needed, but the core logic must be implemented in the C program.