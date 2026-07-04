You are an artifact manager tasked with curating binary repositories for legacy system logs. 

Incoming logs are delivered as split tarball archives and contain files encoded in legacy formats. You must write a C program that continuously watches an incoming directory, processes these split archives upon a trigger, converts their encodings, and packages them into a curated repository.

**Requirements:**
1. Create a C program named `/home/user/curator.c`.
2. The program must use Linux `inotify` to watch the directory `/home/user/incoming/` for the creation of a file named `manifest.done`.
3. When `manifest.done` is detected, the program must:
   - Locate the split archive parts named `artifact.tar.001` and `artifact.tar.002` in `/home/user/incoming/`.
   - Reassemble these parts into a single valid tar archive and extract its contents.
   - Find all extracted files ending with the `.log` extension. These files are strictly encoded in `UTF-16LE`.
   - Read these `.log` files and convert their text encoding from `UTF-16LE` to `UTF-8`.
   - Package *only* the converted `.log` files into a new compressed archive at `/home/user/curated/artifact_curated.tar.gz`. The files in this tarball must not contain absolute paths (e.g., they should be at the root of the tarball or in a relative directory structure).
   - Write a summary file at `/home/user/curated/summary.txt` containing the names of the successfully processed `.log` files, one per line.
   - Exit with status code 0.
4. You may use system commands (via `system()` or `popen()`) within your C code for the archive extraction and creation, but the file watching, directory traversal, and encoding conversion (using the `iconv` API) MUST be done natively in C.
5. Compile your program to `/home/user/curator`.

**Execution sequence:**
Once your code is written and compiled:
1. Start your compiled program in the background (e.g., `./curator &`).
2. Create a file named `/home/user/ready` to signal that your watcher is running.
3. Wait. An automated external process will detect `/home/user/ready`, generate the split archives, and finally create `manifest.done`. Your program should automatically detect this, process the files, create the outputs in `/home/user/curated/`, and exit. 

Ensure both `/home/user/incoming/` and `/home/user/curated/` directories exist before starting your program.