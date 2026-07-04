You are acting as a backup administrator archiving and restoring legacy data. We have a set of custom-compressed backup chunks and a multi-line manifest log detailing the backup jobs. 

Your task is to write a **C program** (and compile/run it) that parses the manifest log, extracts and decompresses the successful backup files, and restores them to a specific directory with appropriate symbolic links.

**System State & Input Files:**
1. **Manifest Log**: Located at `/home/user/backup_manifest.log`.
   It contains multi-line records formatted exactly like this, separated by a blank line:
   ```
   Job-ID: 1001
   Archive: /home/user/backups/data_A.bin
   Status: SUCCESS
   
   Job-ID: 1002
   Archive: /home/user/backups/data_B.bin
   Status: FAILED
   ```

2. **Backup Archives**: Located in `/home/user/backups/`. 
   These are custom binary files with the following structure:
   - **Header (36 bytes total)**:
     - Bytes 0-3: Magic number `BKUP` (ASCII).
     - Bytes 4-35: Original filename, max 32 bytes, null-padded ASCII string (e.g., `report.txt`).
   - **Payload (Variable length)**:
     - Run-Length Encoded (RLE) compressed data. 
     - Every 2 bytes represents a run: `[Count (uint8_t)][Character (ASCII)]`.
     - For example, the bytes `0x03 0x41` should decompress to `AAA`.

**Your Goal:**
Write a C program (save it as `/home/user/restore.c`) that:
1. Reads `/home/user/backup_manifest.log`.
2. Identifies all records where `Status: SUCCESS`.
3. For each successful job, opens the corresponding `.bin` file from the `Archive:` field.
4. Validates the `BKUP` magic number. If invalid, skip the file.
5. Extracts the original filename from the header.
6. Decompresses the RLE payload and writes the uncompressed string to `/home/user/restored/<original_filename>`.
7. Creates a symbolic link at `/home/user/restored/job_<Job-ID>.link` that points to the restored file (`/home/user/restored/<original_filename>`).

**Constraints & Notes:**
- Create the `/home/user/restored` directory before writing to it.
- Compile your C code with `gcc` and run it to perform the actual restoration.
- You do not need to process `FAILED` jobs.
- The C program should handle standard POSIX file operations.