You are an artifact manager responsible for curating binary repositories. We have a set of legacy binary artifacts that contain a deprecated telemetry signature. You need to identify the correct artifacts, strip the signature in-place using memory-mapped I/O, and create an incremental backup of the modifications.

Here are the specific requirements:

1. **Manifest Parsing**: 
   You have a raw manifest file at `/home/user/manifest.raw`. It contains tabular data separated by `|`, with columns: `ArtifactName | Version | Architecture | Status`. 
   Use `awk`, `sed`, or other text transformation tools to extract the `ArtifactName` of all artifacts where the `Status` column exactly matches `NEEDS_PATCH`. Save this list of filenames, one per line, to `/home/user/targets.txt`.

2. **Binary Transformation (C Program)**:
   Write a C program at `/home/user/patcher.c` that does the following:
   - Reads a list of filenames from a file (pass `/home/user/targets.txt` to it).
   - Opens each file located in the `/home/user/artifacts/` directory.
   - Uses memory-mapped I/O (`mmap` with `MAP_SHARED`, `PROT_READ | PROT_WRITE`) to map the entire file into memory.
   - Scans the memory-mapped file for a specific 8-byte deprecated signature: `0xDE, 0xAD, 0xBE, 0xEF, 0xCF, 0xFA, 0xED, 0xFE`.
   - Replaces EVERY instance of this signature in the file with 8 null bytes: `0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00`.
   - Safely unmaps and closes the file.
   Compile this program to `/home/user/patcher` and execute it.

3. **Incremental Backup**:
   A base backup of the `/home/user/artifacts` directory has already been created, and its tar snapshot file is located at `/home/user/backup_snapshot.snar`. 
   After you have successfully patched the binaries, create an incremental `tar` backup named `/home/user/patch_incremental.tar` using the existing snapshot file `/home/user/backup_snapshot.snar` to capture *only* the files that were modified by your C program.

4. **Logging**:
   Output the list of files successfully included in the incremental backup to `/home/user/backup_contents.txt` (you can get this by running `tar -tf /home/user/patch_incremental.tar`).

Constraints:
- You must use `mmap` for the binary modification. Standard `read`/`write` calls for the replacement are not allowed.
- Do not modify files in `/home/user/artifacts/` that are not listed as `NEEDS_PATCH` in the manifest.