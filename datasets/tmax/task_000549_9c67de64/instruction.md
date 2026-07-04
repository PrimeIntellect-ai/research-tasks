You are managing a repository of compiled artifacts. We have a set of custom binary artifact files, a list of deprecated modules, and a backup archive. 

Your task is to write a C program to extract metadata from the binaries, write an inventory safely, process deprecations using shell tools, and verify the backup archive.

Here are the specific steps:

1. **Extract Headers via C**:
   Write a C program at `/home/user/extract_headers.c` and compile it to `/home/user/extract_headers`. The program should scan all `.art` files in the directory `/home/user/artifacts/`.
   Each `.art` file has the following binary header structure:
   - Bytes 0-3: Magic bytes `ARTF` (ASCII)
   - Bytes 4-7: Version (32-bit unsigned integer, little-endian)
   - Bytes 8-39: Artifact Name (32-byte null-terminated ASCII string)
   - Bytes 40-43: Payload size in bytes (32-bit unsigned integer, little-endian)
   - Bytes 44+: Payload data (ignore this)
   
   The C program must extract this metadata and write it to `/home/user/inventory.csv`. Format each line as:
   `filename,Artifact_Name,Version,Payload_size`
   (e.g., `alpha.art,Alpha-Build,1,1024`).
   
   **Important:** The write operation in your C program must be **atomic**. You must write the output to a temporary file (`/home/user/inventory.csv.tmp`) first, and then atomically rename it to `/home/user/inventory.csv`.

2. **Filter Deprecated Artifacts**:
   You have a text file at `/home/user/deprecated.txt`. It contains various notes, but any line containing the exact string `DEPRECATED: ` followed by an artifact name means that artifact is no longer supported.
   Using standard text transformation tools (`awk`, `sed`, or `grep`), read `/home/user/deprecated.txt`, find the deprecated artifact names, and filter them out of `/home/user/inventory.csv`. 
   Write the resulting cleaned inventory to `/home/user/final_inventory.csv`.

3. **Archive Verification**:
   There is a backup archive at `/home/user/backup.tar.gz`. Verify its integrity. If the archive is perfectly intact, write the string `OK` to `/home/user/backup_status.txt`. If it is corrupted or fails verification, write `CORRUPT` to `/home/user/backup_status.txt`.

Ensure your C code compiles cleanly and your final files match the requested paths exactly.