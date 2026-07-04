You are helping a developer organize their project files and secure a custom archive extraction tool. 

In `/home/user/project`, there is a C source file `extractor.c`. This program reads a custom archive format from standard input and writes the files to the current directory. The archive format is a sequence of entries:
`[filename] [size_in_bytes]\n[data]`

However, `extractor.c` has a directory traversal (zip slip) vulnerability. It blindly trusts the `[filename]` provided in the archive, which could allow an attacker to overwrite files outside the intended directory by using `../` or absolute paths (e.g., `/etc/passwd`).

Your tasks are:
1. **Fix `extractor.c`**: Modify the C code so that if a filename contains the substring `../` or starts with `/`, the program **skips** writing that file (it must still consume the `size` bytes from the stream so subsequent files are parsed correctly). Do not write anything to the disk for skipped files.
2. **Compile**: Compile the fixed `extractor.c` into an executable named `extractor` in `/home/user/project`.
3. **Extract**: There is a compressed archive `/home/user/project/archive.gz`. Process this compressed stream and pipe the decompressed data into your compiled `./extractor`. 
4. **Parse and Backup**: The extraction will produce a configuration file named `backup.conf` in the current directory (`/home/user/project`). This file contains a list of filenames (one per line). Create a directory `/home/user/project/backup_dir`. For every file listed in `backup.conf` that exists in `/home/user/project`, create a **hard link** to it inside `/home/user/project/backup_dir/`.
5. **Log**: Create a file `/home/user/project/success.log` containing the exact word `COMPLETED` when you are done.

Ensure you run your extraction and backup commands from within `/home/user/project`.