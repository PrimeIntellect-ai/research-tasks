You are tasked with organizing a messy, nested project backup for a developer. 

In `/home/user/`, you will find a compressed backup named `project_backup.tar.gz` and a configuration file named `rules.ini`. 

Your goal is to complete the following phases:

**Phase 1: Nested Extraction**
The `project_backup.tar.gz` archive contains files, directories, and further nested archives (specifically `.zip` and `.tar` files). You must extract the root archive and recursively extract any nested archives inside it until all actual files are exposed. Place all fully extracted contents (ignoring the leftover archive files themselves) into a directory you must create at `/home/user/raw_files/`.

**Phase 2: The C++ Organizer**
Write a C++17 program at `/home/user/sorter.cpp`. This program must:
1. Parse `/home/user/rules.ini`. The file contains lines in the format `KEY=DESTINATION_DIR`.
2. Recursively traverse the `/home/user/raw_files/` directory.
3. For each regular file found, read its contents to determine its type:
   - If the first 4 bytes of the file exactly match the hexadecimal magic number `0xDE 0xCA 0xFB 0xAD`, it is a "MODULE".
   - If the first 4 bytes do NOT match the magic number, but the first 10 bytes of the file consist entirely of printable ASCII characters (hex 0x20 to 0x7E, plus newlines `\n`), it is "TEXT".
   - Ignore any files that do not match these two categories.
4. If a file is a MODULE, move it to the directory specified by the `MODULE_DIR` key in `rules.ini`. If it is TEXT, move it to the directory specified by the `TEXT_DIR` key. Create these destination directories if they do not exist.
5. For every file moved, output a log to `stdout` in the exact format: `[SUCCESS] Moved <filename> to <destination_path>` (e.g., `[SUCCESS] Moved data.bin to /home/user/organized/modules`).

**Phase 3: Execution**
1. Compile your C++ program using g++ (name the executable `sorter`).
2. Run the program, and use standard stream redirection to pipe the output into a log file at `/home/user/sort.log`. 

*Note: Ensure your C++ program handles standard file I/O and directory traversal efficiently. You are expected to use Bash tools/scripts for Phase 1 and C++ for Phase 2.*