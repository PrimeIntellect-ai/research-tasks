You are a performance engineer tasked with recovering a corrupted sensor database and profiling an application that processes it. 

The system experienced a crash, leaving the main SQLite database corrupted, but an SQL dump of the older state and a custom Write-Ahead Log (WAL) of the latest events survived.

You have the following files in `/home/user/`:
- `backup.sql`: A partial SQL dump of the sensor database prior to the crash.
- `recovery.wal`: A custom text-based WAL file containing the events that occurred after the backup. Each line is formatted as: `INSERT|<id>|<value>|<timestamp>|<timezone_string>`.
- `analyzer.c`: A C program that reads the database and calculates the total sum of the sensor values per hour. It compiles with `gcc analyzer.c -o analyzer -lsqlite3`.

Perform the following steps:
1. **Database Recovery**: Recreate the SQLite database at `/home/user/sensor_data.db` by first loading `backup.sql`, then parsing `recovery.wal` and inserting the missing rows into the `sensors` table.
2. **Performance Profiling**: The `analyzer` program works but is incredibly slow. Use system call tracing (e.g., `strace`) to profile the compiled `analyzer` binary running against `sensor_data.db`. Identify the file-related system call and the corresponding file path that is causing the bottleneck due to a subtle timezone handling bug in the C code.
3. **Bottleneck Reporting**: Create a file at `/home/user/bottleneck.txt` containing exactly one line with the format `<syscall>:<filepath>`, identifying the redundant operation (e.g., `openat:/etc/localtime`).
4. **MRE Creation**: Create a Minimal Reproducible Example in C at `/home/user/mre.c` that isolates the bug found in `analyzer.c` (it should simply execute the problematic sequence of timezone-related library calls in a loop of 10,000 iterations without any SQLite code).
5. **Fix and Execute**: Fix the bug in `/home/user/analyzer.c` so that it avoids redundant system calls (for example, by only updating the timezone when it actually changes between rows). Recompile and run it. Save the program's standard output to `/home/user/output.txt`.

Constraints:
- Do not change the final calculation logic of `analyzer.c`.
- You must use C to fix `analyzer.c` and write `mre.c`.