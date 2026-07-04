You are a backup administrator tasked with recovering a critical application's state from a legacy, proprietary backup system. The backup is stored in a mixed text/binary format, and a subsequent differential backup must be applied to restore the system to its final correct state.

You must write standard C programs (using only the C standard library and POSIX standard functions available on a typical Linux system) to process these custom formats. Shell scripts may be used for compilation and standard system administration tasks (like extracting tarballs), but the parsing and patching logic must be implemented in C.

**Phase 1: Extracting the Base Archive**
The initial full backup is stored in `/home/user/backups/raw_dump.dat`. This file contains multi-line text system logs interleaved with binary chunks of a `tar.gz` archive. 
You must write a C program, `/home/user/extractor.c`, that parses `raw_dump.dat` and reconstructs the archive.
* The file contains arbitrary text lines.
* A binary chunk is strictly bounded by specific marker lines. 
* The start marker is exactly `[CHUNK_START:<size>]\n` (where `<size>` is the integer number of bytes of the binary payload).
* Immediately following the newline of the start marker is the raw binary data.
* Immediately following the binary data is a newline, and then the end marker `[CHUNK_END]\n`.
* You must extract all binary chunks in the order they appear and concatenate them into a single file at `/home/user/merged.tar.gz`.

**Phase 2: Base Restoration**
Using standard Linux tools, extract `/home/user/merged.tar.gz` into the directory `/home/user/restore/`. (The tarball contains files at its root, not inside a parent folder).

**Phase 3: Applying Differential Backups**
A differential backup manifest is located at `/home/user/backups/differential.log`. It contains multi-line records defining operations to apply to the files in `/home/user/restore/`.
Write a C program, `/home/user/patcher.c`, that parses this log and applies the changes.
The log contains records separated by a line containing exactly `---`. 
Each record consists of key-value pairs separated by `: ` (colon and a space).
Operations can be:
1. `OPERATION: DELETE`
   `TARGET: <relative/path/to/file>`
   Action: Delete the file inside `/home/user/restore/`.
2. `OPERATION: APPEND`
   `TARGET: <relative/path/to/file>`
   `SOURCE: <absolute/path/to/source_file>`
   Action: Append the exact raw binary/text contents of the `SOURCE` file to the `TARGET` file inside `/home/user/restore/`.

**Phase 4: Verification**
Once the restoration and patching are fully complete, calculate the SHA-256 hashes of all the files currently remaining in `/home/user/restore/`. 
Write the output to `/home/user/final_hashes.txt` using the command:
`cd /home/user/restore && find . -type f | sort | xargs sha256sum > /home/user/final_hashes.txt`

Your tasks are:
1. Write and compile `extractor.c`.
2. Run it to produce `merged.tar.gz` and extract it.
3. Write and compile `patcher.c`.
4. Run it to process `differential.log`.
5. Generate `final_hashes.txt`.