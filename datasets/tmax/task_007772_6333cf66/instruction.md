You are tasked with building a reliable configuration state tracker in C. A background configuration manager constantly updates files in a directory, and you need to safely capture a consistent snapshot of all configurations without reading partial updates.

Write a C program located at `/home/user/config_snapshot.c` and compile it to `/home/user/snapshot`. 

Your C program must perform the following operations:
1. **Metadata-based File Search:** Recursively search the directory `/home/user/configs` for all files ending with the `.conf` extension.
2. **Sorting:** Sort the discovered file paths alphabetically (lexicographically by absolute path) before processing them.
3. **File Locking & Memory-Mapped I/O:** For each `.conf` file:
   - Open the file and immediately acquire a shared read lock using `flock(fd, LOCK_SH)`. This is critical to prevent reading a file while the external configuration manager is writing to it.
   - Map the file into memory using `mmap` (read-only).
   - Write the file's information to a temporary file located at `/home/user/snapshot.tmp`.
   - Unmap the memory, release the lock, and close the file.
4. **Atomic Write:** Once all `.conf` files have been successfully processed and written to `/home/user/snapshot.tmp`, atomically move/rename the temporary file to `/home/user/snapshot.log`.

**Output Format Constraint:**
For every file processed, the temporary file (and ultimately `snapshot.log`) must append the data exactly in this format:
```
FILE: <absolute_path>
CONTENT:
<exact_file_content>
EOF
```

For example, if `/home/user/configs/app.conf` contains `port=8080`, the output would include:
```
FILE: /home/user/configs/app.conf
CONTENT:
port=8080
EOF
```

**Execution:**
Once you have written and compiled the program to `/home/user/snapshot`, run it so that it produces the final `/home/user/snapshot.log` file. 

*Note: Ensure your C program handles standard error checking. You may use any standard C library headers (e.g., `<dirent.h>`, `<sys/mman.h>`, `<sys/file.h>`, `<fcntl.h>`, `<unistd.h>`).*