You are a storage administrator managing a large-scale data ingestion pipeline. Recently, an automated archive extraction script caused a critical security incident similar to "Zip Slip" by writing files outside the intended destination directory due to un-sanitized path traversal characters (`../`). 

Your task is to implement a secure, high-performance file reorganization daemon in C to replace the flawed script. 

Write a C program named `/home/user/secure_archiver.c` and compile it to `/home/user/secure_archiver`. 

**Daemon Specifications:**
1. **File Watching:** Use `inotify` to monitor the directory `/home/user/spool` for new `.map` files (specifically `IN_CLOSE_WRITE` or `IN_MOVED_TO`).
2. **Memory-Mapped I/O:** When a `.map` file is detected, use `mmap` to read its contents efficiently. These files can be large (bulk renaming instructions).
3. **Parsing:** The `.map` file contains newline-separated instructions in the format:
   `SOURCE_FILENAME:TARGET_RELATIVE_PATH`
   (e.g., `data_001.bin:project_alpha/data.bin` or `data_002.bin:dir/../malicious/data.bin`)
4. **Path Sanitization & Manipulation:** 
   - All source files reside in `/home/user/staging/`.
   - The intended destination base is `/home/user/vault/`.
   - You must evaluate `TARGET_RELATIVE_PATH`. It may contain `../` components.
   - **Crucial:** You must logically resolve the target path to ensure it absolutely does NOT escape `/home/user/vault/`. 
   - If the resolved path attempts to write outside `/home/user/vault/` (e.g., resolving to `/home/user/escaped.bin`), you must block the operation.
   - If the path is safe, allow it.
5. **Bulk Renaming & Directory Creation:** 
   - For allowed operations, create any necessary missing subdirectories inside `/home/user/vault/` using appropriate permissions (0755).
   - Move the file from `/home/user/staging/SOURCE_FILENAME` to the resolved safe path in `/home/user/vault/`.
6. **Audit Logging:** Append the outcome of every instruction to `/home/user/security.log` in the exact format:
   `[BLOCKED] SOURCE_FILENAME -> TARGET_RELATIVE_PATH` (if it escapes the vault)
   `[MOVED] SOURCE_FILENAME -> RESOLVED_ABSOLUTE_PATH` (if successful)
7. **Cleanup & Termination:** Delete the processed `.map` file. If a file named exactly `SHUTDOWN` appears in `/home/user/spool/`, the daemon must gracefully exit.

**Execution Steps:**
1. Write and compile the C code.
2. We have pre-generated a massive mapping file at `/home/user/test_batch.map` and thousands of dummy files in `/home/user/staging/`.
3. Start your compiled `secure_archiver` daemon in the background.
4. Move `/home/user/test_batch.map` into `/home/user/spool/` to trigger the bulk processing.
5. Wait for processing to finish, then touch `/home/user/spool/SHUTDOWN` to terminate your daemon.
6. Ensure the daemon has completely exited.