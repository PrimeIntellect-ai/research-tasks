You are tasked with writing a C program to help organize and reassemble a heavily fragmented project workspace, while ensuring security against path traversal attacks (similar to "zip slip").

The project files are currently stored in chunks in `/home/user/spool/chunks/`. 
New files are scheduled to be reassembled via manifest files dropped into `/home/user/spool/manifests/`.

Your goal is to write a C program at `/home/user/organizer.c` and compile it to `/home/user/organizer`. This program must run continuously and watch the `/home/user/spool/manifests/` directory for new manifest files.

### Program Requirements

**1. File Watching**
Use `inotify` to monitor `/home/user/spool/manifests/`. When a new file with a `.manifest` extension is completely written (e.g., `IN_CLOSE_WRITE`), the program should process it. 

**2. Manifest Parsing**
The manifest files are plain text with the following format:
*   Line 1: `DEST:<relative_path>` (The target path relative to the safe directory `/home/user/project_root/`)
*   Line 2: `CHUNKS:<N>` (The number of chunks)
*   Lines 3 to N+2: Exact absolute paths to the chunk files, in the order they must be merged.
*   Line N+3: `CHECKSUM:<sum>` (An integer representing the sum of all bytes in the final merged file, modulo 256).

**3. Security and Path Sanitization (Zip Slip Prevention)**
Before merging, your program must check the `DEST` relative path. If the path attempts to break out of `/home/user/project_root/` (e.g., by using `../` components that resolve above the root), the program MUST NOT write the file. 
Instead, it must append a line to `/home/user/logs/security.log` in the exact format:
`VIOLATION: <relative_path>`

**4. Merging and Checksum Verification**
If the path is safe, read the specified chunk files in order. Calculate the checksum of the combined bytes (sum of all bytes modulo 256). 
*   If the calculated checksum matches the `CHECKSUM` in the manifest, write the merged data to `/home/user/project_root/<relative_path>`. Create any necessary intermediate directories.
*   If the checksum does NOT match, do not write the file. Append a line to `/home/user/logs/security.log` in the exact format:
`CHECKSUM_ERROR: <relative_path>`

### Instructions for the Agent
1. Create the directories `/home/user/spool/manifests/`, `/home/user/spool/chunks/`, `/home/user/project_root/`, and `/home/user/logs/`.
2. Write the C program `/home/user/organizer.c`.
3. Compile it: `gcc -o /home/user/organizer /home/user/organizer.c`
4. Run the program in the background: `/home/user/organizer &`
5. Once your program is running, you must trigger the test script we have pre-installed at `/home/user/drop_manifests.sh` (this script does not exist yet, you must wait to run it, but assume it will drop test files into the manifests directory). Wait 5 seconds after running the script to allow your daemon to process the files before finishing.