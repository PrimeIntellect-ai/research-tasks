You are a Site Reliability Engineer investigating a sudden crash in a custom uptime monitoring daemon. The daemon writes state changes to a custom binary Write-Ahead Log (WAL). Recently, the daemon crashed and has been unable to restart. 

Here is what we know:
1. The daemon source code is located at `/home/user/app/daemon.py`.
2. The crashed application's binary log file is at `/home/user/app/wal.dat`.
3. The application crash log is at `/home/user/app/error.log`. 
4. The binary log file format is supposed to be a sequence of records. Each valid record begins with a specific 4-byte magic header, followed by a timestamp, and a status indicator.
5. We suspect two issues: 
   - A recent disk failure corrupted a small portion of `wal.dat`. You will need to recover the database by skipping the corrupted bytes and resyncing the parser to the next valid magic header.
   - The daemon relies on a specific encoding and serialization format, but it appears to be incorrectly parsing high-value timestamps, leading to negative duration calculations (a precision/overflow issue) which crashes the daemon.

Your task:
1. Analyze the stack trace and the codebase.
2. Identify and fix the serialization/unpacking bug in the Python script.
3. Modify the script to handle database recovery from the corrupted `wal.dat` file by scanning for the magic bytes (`0xDEADBEEF`) to skip over unreadable/corrupted sections.
4. Run your fixed script to parse the entire `wal.dat` file.
5. Calculate the total cumulative uptime in milliseconds. (Uptime is the sum of all durations where the status was `UP` (1). A state lasts until the next state change).
6. Save ONLY the final total uptime in milliseconds as an integer in `/home/user/uptime_result.txt`.

Ensure your fix correctly tracks precision and handles the binary encoding correctly.