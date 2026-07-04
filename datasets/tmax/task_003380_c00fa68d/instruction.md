You are an artifact manager curator for a local binary repository. Your task is to write a C program that automatically ingests newly uploaded binary artifacts, verifies them using memory-mapped I/O, deduplicates them, and safely links them into a repository structure using atomic operations.

You must write a C program at `/home/user/curator.c` and compile it to `/home/user/curator`. 

The program should perform the following operations:
1. Initialize the repository structure. Ensure the following directories exist:
   - `/home/user/repo/incoming`
   - `/home/user/repo/objects`
   - `/home/user/repo/by-name`

2. Run as a continuous process (or daemon) that uses `inotify` to monitor the `/home/user/repo/incoming/` directory for `IN_CLOSE_WRITE` events (which indicates a file has finished writing).

3. When a new file is detected:
   - Map the file into memory using `mmap`.
   - Compute a custom 32-bit checksum of the file. The checksum is defined as the simple sum of all bytes in the file, modulo `0x100000000` (i.e., keep the lower 32 bits of the sum). Represent this checksum as a zero-padded 8-character lowercase hex string (e.g., `00a1b2c3`).
   - Create the artifact in the objects directory atomically: Write the file contents to a temporary file in `/home/user/repo/objects/` (e.g., `temp_XXXXXX`), and then use `rename()` to atomically move it to `/home/user/repo/objects/<checksum>`.
   - Create or update a symbolic link at `/home/user/repo/by-name/<original_filename>` that points to the object file `../objects/<checksum>`. If the symlink already exists, it must be updated atomically (e.g., create a temp symlink and rename it over the old one).
   - Atomically update a file at `/home/user/repo/latest.txt` to contain strictly the `<checksum>` of the most recently processed artifact, followed by a newline. Do this by writing to a temporary file and renaming it.
   - Finally, delete the original file from `/home/user/repo/incoming/`.

Constraints & Instructions:
- Write the code in C. Use `gcc -O2 /home/user/curator.c -o /home/user/curator` to compile it.
- After compiling, execute the program in the background so it is actively watching the directory. You can test it yourself by dropping a file into `/home/user/repo/incoming/`. Leave the program running in the background when you finish the task.
- The daemon should handle multiple files being dropped into the incoming directory sequentially.
- Standard libraries only (POSIX, `<sys/inotify.h>`, `<sys/mman.h>`, etc.). Do not use external libraries like `libcrypto`.