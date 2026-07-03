You are a performance and systems engineer tasked with recovering critical application data and fixing a serialization bug in a C profiling tool. 

A recent system crash corrupted our main SQLite database located at `/home/user/data/metrics.db`. We rely on the Write-Ahead Log (WAL) to recover the latest entries. Additionally, the C application that generates these metrics (`/home/user/profiler_app`) has a severe performance bug related to binary data serialization/endianness, and it seems an encryption key was temporarily hardcoded in the repository before being removed.

Your objectives:
1. **Database Recovery**: The database `/home/user/data/metrics.db` is corrupted, but the WAL file (`metrics.db-wal`) is intact. Recover the database and extract the value of the `payload` column from the `events` table where `event_type` is `'critical_crash'`. The payload is stored as a hex-encoded string.
2. **Git Forensics**: Inspect the Git repository at `/home/user/profiler_app`. Find the commit where a hardcoded XOR encryption key was removed. 
3. **Fix the C Code**: The repository contains a program `decoder.c` intended to decode the payload. However, it contains a serialization/endianness bug that causes it to hang or allocate excessive memory when parsing the data length, leading to a performance bottleneck. Fix the C code so it correctly reads the 32-bit length prefix (which is stored in little-endian format in the binary data, but the code incorrectly processes it) and successfully XOR-decrypts the hex payload using the key found in the Git history.
4. **Decoding**: Compile your fixed `decoder.c` and use it to decode the extracted payload with the recovered key. 

Save the final decrypted string to `/home/user/solution.txt`.

Note: You can use standard tools like `sqlite3`, `git`, `gcc`, and `gdb`.