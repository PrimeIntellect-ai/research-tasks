You are an IT Support Escalation Technician. We have an urgent ticket (Ticket #8492). 

A critical internal service, the "WAL-Recovery-Daemon", is crashing repeatedly on startup. The daemon reads a custom Write-Ahead Log (WAL) to recover state after a crash. Unfortunately, due to a recent power outage, the `data.wal` file was partially corrupted. Now, every time the daemon tries to start, it encounters this corrupted file, exhausts system resources (stack overflow), and crashes.

Your workspace is located at `/home/user/ticket_8492`. In this directory, you will find:
- The source code for the daemon (`main.cpp`, `wal_parser.cpp`, `wal_parser.h`)
- A `Makefile`
- The corrupted WAL file (`data.wal`)

Your tasks to resolve this ticket:
1. **Error Diagnosis & Fixing:** Debug the daemon to understand why it crashes when reading `data.wal`. Identify the logic bug in `wal_parser.cpp` causing the infinite recursion/loop when it encounters a corrupted (zero-length) record. Modify `wal_parser.cpp` so that if it encounters an invalid record length (0), it aborts processing that specific file gracefully, skipping the rest of the corrupted file, but returning all successfully parsed records up to that point.
2. **Database Recovery:** Run the patched daemon using the `Makefile` (run `make`, then `./wal_daemon data.wal`). The fixed daemon will process `data.wal` and automatically write the successfully recovered records to `/home/user/ticket_8492/recovered.txt`. 
3. **Regression Test:** Write a bash script at `/home/user/ticket_8492/regression_test.sh` that:
   - Compiles the daemon.
   - Creates a dummy corrupted WAL file named `test_corrupt.wal` (you can design its contents, but it must trigger the original bug if tested against the old code).
   - Runs `./wal_daemon test_corrupt.wal`.
   - Checks the exit code. The script must exit with code 0 if the daemon exits successfully (i.e., gracefully handles the corruption without crashing), and exit with code 1 if the daemon crashes or fails.

Ensure the final `recovered.txt` contains only the valid data parsed before the corruption.