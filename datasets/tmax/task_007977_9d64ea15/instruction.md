You are assisting a technical writer who organizes documentation for a large open-source project. Multiple automated systems concurrently drop compressed documentation drafts into a specific directory. We need a reliable system to monitor this directory, verify the incoming archives, generate checksums, and safely append the results to a central manifest file without race conditions.

Your task is to implement this system using a combination of a bash script and a C program.

**Requirements:**

1. **C Program (`/home/user/doc_parser.c`):**
   Write a C program that takes exactly two arguments: the path to an incoming archive file, and the path to a manifest file.
   Usage: `./doc_parser <path_to_archive> <path_to_manifest>`
   
   The program must perform the following actions:
   * **Archive Integrity:** Check if the incoming file is a valid GZIP archive by reading its first two bytes (the "magic number"). A valid GZIP file must start with `0x1F` followed by `0x8B`.
   * **Checksum Generation:** If the file is a valid GZIP archive, calculate its SHA-256 checksum. You may use `popen` to call the system `sha256sum` utility.
   * **Concurrent Access / File Locking:** Open the manifest file for appending. Before writing, acquire an exclusive write lock using POSIX `fcntl` (`F_SETLKW`). 
   * **Data Parsing & Appending:** 
     * If the archive is valid, append the following line to the manifest:
       `<basename_of_archive> <sha256_hash> VALID`
     * If the archive is invalid (does not start with `0x1F 0x8B`), append:
       `<basename_of_archive> INVALID`
   * Release the lock and close the file.
   
   Compile this C program to `/home/user/doc_parser`. Ensure it compiles without errors.

2. **File Watching Bash Script (`/home/user/watch.sh`):**
   Write a bash script that uses `inotifywait` to monitor the directory `/home/user/docs/`.
   * It should continuously watch for `close_write` events.
   * Whenever a new file is written and closed in `/home/user/docs/`, the script must execute the `/home/user/doc_parser` program, passing the full path of the new file and `/home/user/manifest.txt` as arguments.
   * The script should be executable (`chmod +x`).

**System State Before You Start:**
* Directory `/home/user/docs/` exists.
* File `/home/user/manifest.txt` exists (initially empty).
* `inotify-tools` is available (you may need to install it).

Provide both the C code and the bash script, make sure they are placed in `/home/user/`, and compile the C program. Do not run the watcher script in the foreground in your final state, as the automated test will invoke it to verify your solution.