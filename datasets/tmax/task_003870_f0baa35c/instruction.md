You are acting as a backup administrator. Our custom storage engine generates a Write-Ahead Log (WAL) that we need to parse to safely archive the stored files. 

Your task is to write a C program at `/home/user/wal_archiver.c` that parses a domain-specific WAL file, extracts the embedded file data, validates it, and appends it to a consolidated binary archive using POSIX file locks to prevent concurrent corruption.

The WAL file is located at `/home/user/backups/db.wal`. 

**WAL Format Description:**
1. The file starts with a magic header: `BKWAL1\n`
2. This is followed by a series of records. Each record consists of a multi-line text header, raw binary data, and a footer:
   - `BEGIN\n`
   - `FILE: <absolute_path>\n`
   - `SIZE: <size_in_bytes>\n`
   - `CHECKSUM: <2-character_hex_string>\n`
   - `DATA\n`
   - `<raw_binary_data_exactly_SIZE_bytes_long>`
   - `END\n`

**Checksum Validation:**
The CHECKSUM is a simple 8-bit sum of all the bytes in the `<raw_binary_data...>` payload modulo 256, represented as a zero-padded 2-character uppercase hex string (e.g., `1A`, `FF`, `00`). Your C program must compute this checksum for each record's data. If the checksum matches, proceed to archive the record. If it does not match, skip the record entirely.

**Archiving Process:**
For each valid record, you must append the data to a binary archive file located at `/home/user/backups/archive.bin`.
Because other backup processes might write to this archive simultaneously, your program **must** acquire an exclusive POSIX write lock (using `fcntl` and `F_WRLCK`) on `archive.bin` before writing each record, and release the lock immediately after.

**Archive Binary Format (Little-Endian):**
For each valid record appended to `archive.bin`, write exactly:
1. `path_length` (uint32_t): The length of the file path string (excluding null terminator).
2. `path` (char array): The file path string (do NOT write a null terminator).
3. `data_size` (uint32_t): The size of the binary data.
4. `data` (byte array): The raw binary data.

**Logging:**
Whenever a valid record is successfully written to the archive, append a line to `/home/user/backups/process.log` in the exact format:
`ARCHIVED <absolute_path> <size_in_bytes> bytes`

**Instructions:**
1. Create the necessary directories if they don't exist. (Assume `/home/user/backups/db.wal` is already provided by the environment).
2. Write the C code to `/home/user/wal_archiver.c`.
3. Compile it to `/home/user/wal_archiver`.
4. Run the archiver on `/home/user/backups/db.wal`.